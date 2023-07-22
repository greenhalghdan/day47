from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import os
amazon_url = "https://www.amazon.co.uk/Logitech-Mechanical-Wireless-Illuminated-Keyboard/dp/B07W7KV4GH/ref=sr_1_4?keywords=mx+keys+mechanical&qid=1690043654&sprefix=mx+keys%2Caps%2C102&sr=8-4"
TARGETPRICE = 50
FROM_ADDR = os.environ.get("FROM_ADDR")
EMAIL = os.environ.get("user")
PASSWORD = os.environ.get("pass")
TO_ADDRESS = os.environ.get("TO_ADDRESS")
amazon_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get(url=amazon_url, headers=amazon_header)
web_page = response.text
soup = BeautifulSoup(web_page, "lxml")
price_whole = soup.find("span", class_="a-price-whole")
price_decimal = soup.find("span", class_="a-price-fraction")
price = float(price_whole.get_text() + price_decimal.get_text())

if price < TARGETPRICE:
    print("true")
    with smtplib.SMTP("eu-smtp-outbound-1.mimecast.com", 587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=FROM_ADDR,
                            to_addrs=TO_ADDRESS,
                            msg=f"subject: Your item is at the right price!\n\nJust to let you know {amazon_url} is now"
                                f" at your target price")