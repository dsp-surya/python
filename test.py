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
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64: x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(url)
time.sleep(3)
html_content = driver.page_source
driver.quit()
tb = pd.read_html(html_content)
ipo_df = tb[0]
ipo_df.columns = ['Name', 'GMP', 'Rating', 'Sub', 'Price', 'IPO Size',
       'Lot', 'Open', 'Close', 'BoA Dt', 'Listing', 'Updated-On',
       'Anchor']

print(ipo_df)

# Configurable settings
SENDER_EMAIL = "testing0357a@gmail.com"
APP_PASSWORD = "wezqrxezjkstloth"  # Use your app password here
RECIPIENT_EMAIL = "testing0357a@gmail.com"

# Construct the email
msg = EmailMessage()
msg["Subject"] = "Hello from Python!"
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg.set_content("This is a plain-text email sent directly from a Python script.")

# Connect to the SMTP server and send
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")