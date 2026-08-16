import os
import re
import time
import smtplib
import warnings
from io import StringIO
from functools import wraps
from email.message import EmailMessage
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings('ignore', category=UserWarning)

URL = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

def retry_on_exception(retries=3, delay=5, backoff=2):
    """Retries a function upon failure with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        print(f"[Error] Final attempt ({attempt}/{retries}) failed: {e}")
                        raise e
                    print(f"[Warning] Attempt {attempt}/{retries} failed ({e}). Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def get_browser_driver() -> webdriver.Chrome:
    """Configures headless Chrome with anti-bot evasion settings."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

@retry_on_exception(retries=3, delay=5, backoff=2)
def fetch_ipo_dataframe() -> pd.DataFrame:
    """Scrapes raw IPO table after waiting explicitly for dynamic content to render."""
    driver = get_browser_driver()
    try:
        driver.get(URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(2)
        html_content = driver.page_source
    finally:
        driver.quit()

    tables = pd.read_html(StringIO(html_content))
    print(f"Scraped {len(tables)} tables from page.")

    target_df = None
    for idx, tbl in enumerate(tables):
        col_str = " ".join([str(c) for c in tbl.columns]).lower()
        if 'gmp' in col_str or 'ipo' in col_str:
            target_df = tbl
            print(f"Matched main IPO table at index {idx} with shape {tbl.shape}")
            break

    if target_df is None:
        print("[Warning] No table matching IPO criteria was found.")
        return pd.DataFrame()

    if isinstance(target_df.columns, pd.MultiIndex):
        target_df.columns = [' '.join(col).strip() for col in target_df.columns.values]

    if len(target_df.columns) == 13:
        target_df.columns = [
            'Name', 'GMP', 'Rating', 'Sub', 'Price', 'IPO Size',
            'Lot', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On', 'Anchor'
        ]
    
    return target_df

def normalize_date_series(series: pd.Series) -> pd.Series:
    """Parses mixed date strings like '18-Aug' or '18-08-2026' into Datetime objects."""
    current_year = pd.Timestamp.today().year
    
    def parse_val(val):
        if pd.isna(val) or not str(val).strip() or str(val).strip() in ['--', '-', 'N/A', 'nan']:
            return pd.NaT
        val_str = str(val).strip()
        if re.match(r'^\d{1,2}-[A-Za-z]{3}$', val_str):
            val_str = f"{val_str}-{current_year}"
        return pd.to_datetime(val_str, errors='coerce', format='mixed')

    return series.apply(parse_val)

def process_and_filter_ipo_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans numeric values, filters active IPOs, and sorts chronologically by close date."""
    if df.empty:
        return df

    print(f"Raw rows before filtering: {len(df)}")

    # Remove completely empty rows or rows missing an IPO Name
    if 'Name' in df.columns:
        df = df[df['Name'].notna()].copy()
        df['Name'] = df['Name'].astype(str).str.strip()
        df = df[~df['Name'].str.lower().isin(['name', '', '--', '-', 'nan'])].copy()

    if df.empty:
        return df

    # Parse Close dates into datetime objects for filtering and sorting
    if 'Close' in df.columns:
        df['_close_dt'] = normalize_date_series(df['Close'])
        today = pd.Timestamp.today().normalize()
        # Keep if Close date is today or in the future, or pending (NaT)
        df = df[(df['_close_dt'] >= today) | (df['_close_dt'].isna())].copy()

    print(f"Rows remaining after date filter: {len(df)}")

    if df.empty:
        return df

    # Extract numeric values safely
    price_num = pd.to_numeric(df['Price'].astype(str).str.extract(r'(\d+)\s*$')[0], errors='coerce')
    lot_num = pd.to_numeric(df['Lot'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
    gmp_val = pd.to_numeric(df['GMP'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)
    sub_num = pd.to_numeric(df['Sub'].astype(str).str.extract(r'(\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)
    
    gmp_pct = (gmp_val / price_num) * 100

    def evaluate_row(pct, val, sub):
        if pd.isna(pct) or val < 0 or pct < 0:
            return "Avoid"
        elif pct >= 15 or (pct >= 10 and sub >= 3):
            return "Apply (Strong)"
        elif pct > 0 or sub >= 1:
            return "May Apply"
        return "Avoid / Risky"

    df['Verdict'] = [evaluate_row(p, v, s) for p, v, s in zip(gmp_pct, gmp_val, sub_num)]
    df['Bid Amount'] = price_num * lot_num

    # Sort chronologically by Close Date (pending dates placed at the end)
    if '_close_dt' in df.columns:
        df = df.sort_values(by='_close_dt', ascending=True, na_position='last')
        df = df.drop(columns=['_close_dt'])

    df = df.drop(columns=['Price', 'Lot'], errors='ignore')
    
    cols = ['Name', 'Verdict', 'GMP', 'Rating', 'Sub', 'IPO Size', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On', 'Anchor', 'Bid Amount']
    return df[[c for c in cols if c in df.columns]]

def build_html_email(df: pd.DataFrame) -> str:
    if df.empty:
        return """
        <html>
          <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
            <h2>Live & Upcoming IPO GMP Updates</h2>
            <p style="color: #718096;">There are currently no active or upcoming IPOs matching today's criteria.</p>
          </body>
        </html>
        """

    headers_html = "".join(f"<th>{col}</th>" for col in df.columns)
    table_rows = []

    for _, row in df.iterrows():
        verdict = str(row.get('Verdict', ''))
        if "Apply (Strong)" in verdict:
            verdict_badge = '<span style="background-color: #276749; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">Apply</span>'
            row_style = 'style="background-color: #f0fff4;"'
        elif "May Apply" in verdict:
            verdict_badge = '<span style="background-color: #d69e2e; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">May Apply</span>'
            row_style = 'style="background-color: #fffff0;"'
        else:
            verdict_badge = '<span style="background-color: #c53030; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">Avoid</span>'
            row_style = 'style="background-color: #fff5f5;"'

        bid_val = row.get('Bid Amount', 0)
        formatted_bid = f"₹{bid_val:,.0f}" if pd.notnull(bid_val) and bid_val > 0 else "-"

        cells = []
        for col in df.columns:
            val = row[col]
            # Replace literal NaN or NaT values with empty dash in table cell
            if pd.isna(val) or str(val).lower() == 'nan':
                cell_str = "-"
            elif col == 'Verdict':
                cell_str = verdict_badge
            elif col == 'Bid Amount':
                cell_str = formatted_bid
            else:
                cell_str = str(val)
            cells.append(f"<td>{cell_str}</td>")
            
        table_rows.append(f"<tr {row_style}>{''.join(cells)}</tr>")

    return f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; font-size: 13px; color: #333; }}
          h2 {{ color: #1a365d; margin-bottom: 10px; }}
          .ipo-table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
          .ipo-table th {{ background-color: #2b6cb0; color: #ffffff; text-align: left; padding: 8px; font-weight: bold; }}
          .ipo-table td {{ border: 1px solid #e2e8f0; padding: 6px 8px; }}
        </style>
      </head>
      <body>
        <h2>Live & Upcoming IPO GMP Report & Verdict</h2>
        <p>Investment recommendations generated based on GMP % return and subscription rates:</p>
        <table class="ipo-table">
          <thead><tr>{headers_html}</tr></thead>
          <tbody>{"".join(table_rows)}</tbody>
        </table>
      </body>
    </html>
    """

def send_email(html_body: str, is_empty: bool, df: pd.DataFrame):
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("APP_PASSWORD")
    recipients_raw = os.environ.get("RECIPIENT_EMAILS", "testing0357a@gmail.com")
    recipients_list = [e.strip() for e in recipients_raw.split(",") if e.strip()]

    if not sender_email or not app_password:
        raise ValueError("Missing SENDER_EMAIL or APP_PASSWORD environment variables.")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients_list)
    msg["Subject"] = "IPO GMP Report - No Active IPOs Today" if is_empty else "Live & Upcoming IPO GMP Report with Verdict"
    
    msg.set_content("No active IPOs found today." if is_empty else f"Live IPO GMP Updates:\n\n{df.to_string()}")
    msg.add_alternative(html_body, subtype='html')

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

def main():
    print("Fetching IPO data...")
    raw_df = fetch_ipo_dataframe()
    
    print("Processing and analyzing metrics...")
    processed_df = process_and_filter_ipo_data(raw_df)
    
    print("Building HTML payload...")
    is_empty = processed_df.empty
    html_body = build_html_email(processed_df)
    
    print("Sending email...")
    send_email(html_body, is_empty, processed_df)
    print("Job completed successfully!")

if __name__ == "__main__":
    main()
