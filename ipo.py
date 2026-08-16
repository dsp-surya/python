import os
import re
import smtplib
from email.message import EmailMessage
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64: x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
time.sleep(3)
html_content = driver.page_source
driver.quit()

tb = pd.read_html(html_content)
ipo_df = tb[0]
ipo_df.columns = ['Name', 'GMP', 'Rating', 'Sub', 'Price', 'IPO Size',
       'Lot', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On',
       'Anchor']

# 1. Filter out past listing dates
today = pd.Timestamp.today().normalize()
parsed_listing_dates = pd.to_datetime(ipo_df['Listing'], errors='coerce')
ipo_df = ipo_df[(parsed_listing_dates >= today) | (parsed_listing_dates.isna())].copy()

# Base email settings
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
RECIPIENT_EMAIL = "testing0357a@gmail.com"

msg = EmailMessage()
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

if ipo_df.empty:
    msg["Subject"] = "IPO GMP Report - No Active IPOs Today"
    msg.set_content("No active or upcoming IPOs found for today.")
else:
    msg["Subject"] = "Live & Upcoming IPO GMP Report with Verdict"
    
    # 2. Extract numeric values for calculations
    price_num = pd.to_numeric(ipo_df['Price'].astype(str).str.extract(r'(\d+)\s*$')[0], errors='coerce')
    lot_num = pd.to_numeric(ipo_df['Lot'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
    
    # Extract absolute GMP numeric value and percentage
    gmp_val = pd.to_numeric(ipo_df['GMP'].astype(str).str.extract(r'(-?\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)
    gmp_pct = (gmp_val / price_num) * 100
    
    # Extract subscription numeric multiplier (e.g., "15.4x" -> 15.4)
    sub_num = pd.to_numeric(ipo_df['Sub'].astype(str).str.extract(r'(\d+(?:\.\d+)?)')[0], errors='coerce').fillna(0)

    # 3. Decision Logic for "Verdict" Column
    def generate_verdict(row_idx):
        pct = gmp_pct.loc[row_idx]
        val = gmp_val.loc[row_idx]
        sub = sub_num.loc[row_idx]
        
        if val < 0 or pct < 0:
            return "Avoid"
        elif pct >= 15 or (pct >= 10 and sub >= 3):
            return "Apply (Strong)"
        elif pct > 0 or sub >= 1:
            return "May Apply"
        else:
            return "Avoid / Risky"

    ipo_df['Verdict'] = [generate_verdict(idx) for idx in ipo_df.index]

    # 4. Add Bid Amount and cleanup columns
    ipo_df['Bid Amount'] = price_num * lot_num
    ipo_df = ipo_df.drop(columns=['Price', 'Lot'])
    ipo_df = ipo_df.sort_values(by='Close', ascending=True)

    # Reorder columns to put Verdict prominently near Name and GMP
    cols = ['Name', 'Verdict', 'GMP', 'Rating', 'Sub', 'IPO Size', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On', 'Anchor', 'Bid Amount']
    display_columns = [c for c in cols if c in ipo_df.columns]

    headers_html = "".join([f"<th>{col}</th>" for col in display_columns])
    table_rows = []

    for _, row in ipo_df.iterrows():
        verdict = row['Verdict']
        
        # Color-code rows/badges based on verdict
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
        for col in display_columns:
            if col == 'Verdict':
                val = verdict_badge
            elif col == 'Bid Amount':
                val = formatted_bid
            else:
                val = row[col]
            cells.append(f"<td>{val}</td>")
            
        table_rows.append(f"<tr {row_style}>{''.join(cells)}</tr>")

    html_table = f"""
    <table class="ipo-table">
      <thead><tr>{headers_html}</tr></thead>
      <tbody>{"".join(table_rows)}</tbody>
    </table>
    """

    email_html = f"""
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
        {html_table}
      </body>
    </html>
    """
    
    msg.set_content(f"Live IPO GMP Updates:\n\n{ipo_df.to_string()}")
    msg.add_alternative(email_html, subtype='html')

# Send Email via SSL
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("Email notification with IPO Verdict sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
