import os
import re
import smtplib
import warnings
from email.message import EmailMessage
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Suppress minor Pandas warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Configuration Constants
URL = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

def get_browser_driver() -> webdriver.Chrome:
    """Configures and returns a lightweight, headless Chrome browser instance."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")  # Speed up page load by disabling images
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_ipo_dataframe() -> pd.DataFrame:
    """Scrapes raw IPO data from the target URL."""
    driver = get_browser_driver()
    try:
        driver.get(URL)
        html_content = driver.page_source
    finally:
        driver.quit()  # Ensures browser process is always terminated cleanly

    tables = pd.read_html(html_content)
    df = tables[0]
    df.columns = [
        'Name', 'GMP', 'Rating', 'Sub', 'Price', 'IPO Size',
        'Lot', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On', 'Anchor'
    ]
    return df

def process_and_filter_ipo_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters, cleans, calculates metrics, and assigns verdicts to the IPO data."""
    if df.empty:
        return df

    # 1. Filter out past listing dates
    today = pd.Timestamp.today().normalize()
    parsed_dates = pd.to_datetime(df['Listing'], errors='coerce', format='mixed')
    df = df[(parsed_dates >= today) | (parsed_dates.isna())].copy()

    if df.empty:
        return df

    # 2. Extract numeric metrics in vectorized operations
    price_num = pd.to_numeric(df['Price'].astype(str).str.extract(r'(\d+)\s*$')[0], errors='coerce')
    lot_num = pd.to_numeric(df['Lot'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
    gmp_val = pd.to_numeric(df['GMP'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)
    sub_num = pd.to_numeric(df['Sub'].astype(str).str.extract(r'(\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)
    
    gmp_pct = (gmp_val / price_num) * 100

    # 3. Decision Verdict Logic
    def evaluate_row(pct, val, sub):
        if val < 0 or pct < 0:
            return "Avoid"
        elif pct >= 15 or (pct >= 10 and sub >= 3):
            return "Apply (Strong)"
        elif pct > 0 or sub >= 1:
            return "May Apply"
        return "Avoid / Risky"

    df['Verdict'] = [evaluate_row(p, v, s) for p, v, s in zip(gmp_pct, gmp_val, sub_num)]
    df['Bid Amount'] = price_num * lot_num

    # 4. Column Cleanup & Sorting
    df = df.drop(columns=['Price', 'Lot']).sort_values(by='Close', ascending=True)
    
    # Reorder display columns
    cols = ['Name', 'Verdict', 'GMP', 'Rating', 'Sub', 'IPO Size', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On', 'Anchor', 'Bid Amount']
    return df[[c for c in cols if c in df.columns]]

def build_html_email(df: pd.DataFrame) -> str:
    """Generates styled HTML content for email delivery."""
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
        verdict = row['Verdict']
        if "Apply (Strong)" in verdict:
            verdict_badge = '<span style="background-color: #276749; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">Apply</span>'
            row_style = 'style="background-color: #f0fff4;"'
        elif "May Apply" in verdict:
            verdict_badge = '<span style="background-color: #d69e2e; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">May Apply</span>'
            row_style = 'style="background-color: #fffff0;"'
        else:
            verdict_badge = '<span style="background-color: #c53030; color: #ffffff; padding: 3px 7px; border-radius: 4px; font-weight: bold;">Avoid</span>'
            row_style = 'style="background-color: #fff5f5;"'

        bid_val = row['Bid Amount']
        formatted_bid = f"₹{bid_val:,.0f}" if pd.notnull(bid_val) and bid_val > 0 else "-"

        cells = []
        for col in df.columns:
            if col == 'Verdict':
                val = verdict_badge
            elif col == 'Bid Amount':
                val = formatted_bid
            else:
                val = row[col]
            cells.append(f"<td>{val}</td>")
            
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
    """Handles SMTP connection and sends the email payload."""
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
