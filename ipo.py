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

price_num = pd.to_numeric(ipo_df['Price'].astype(str).str.extract(r'(\d+)\s*$')[0], errors='coerce')
lot_num = pd.to_numeric(ipo_df['Lot'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')

ipo_df['Bid Amount'] = price_num * lot_num
ipo_df = ipo_df.drop(columns=['Price', 'Lot'])

ipo_df = ipo_df.sort_values(by='Close', ascending=True)

def parse_gmp_status(gmp_str):
    gmp_str = str(gmp_str).strip()
    if '-' in gmp_str:
        return 'negative'
    # Extract numbers from strings like "₹50 (25%)"
    match = re.search(r'(\d+(?:\.\d+)?)', gmp_str)
    if match and float(match.group(1)) > 0:
        return 'positive'
    return 'neutral'

display_columns = [col for col in ipo_df.columns if col != 'Bid Amount'] + ['Bid Amount']

headers_html = "".join([f"<th>{col}</th>" for col in display_columns])
table_rows = []

for _, row in ipo_df.iterrows():
    gmp_status = parse_gmp_status(row['GMP'])
    
    if gmp_status == 'positive':
        row_style = 'style="background-color: #e6fffa; color: #22543d; font-weight: 500;"'  # Soft Green
    elif gmp_status == 'negative':
        row_style = 'style="background-color: #fff5f5; color: #9b2c2c;"'  # Soft Red
    else:
        row_style = ''

    bid_val = row['Bid Amount']
    formatted_bid = f"₹{bid_val:,.0f}" if pd.notnull(bid_val) and bid_val > 0 else "-"

    cells = []
    for col in display_columns:
        val = formatted_bid if col == 'Bid Amount' else row[col]
        cells.append(f"<td>{val}</td>")
        
    table_rows.append(f"<tr {row_style}>{''.join(cells)}</tr>")

html_table = f"""
<table class="ipo-table">
  <thead>
    <tr>{headers_html}</tr>
  </thead>
  <tbody>
    {"".join(table_rows)}
  </tbody>
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
    <h2>Live IPO GMP Updates</h2>
    <p>Rows highlighted in <strong>green</strong> indicate positive GMP gains:</p>
    {html_table}
  </body>
</html>
"""

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
RECIPIENT_EMAIL = "testing0357a@gmail.com"

msg = EmailMessage()
msg["Subject"] = "Live IPO GMP Report (Highlighted)"
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

msg.set_content(f"Live IPO GMP Updates:\n\n{ipo_df.to_string()}")
msg.add_alternative(email_html, subtype='html')

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("Email with highlighted rows sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
