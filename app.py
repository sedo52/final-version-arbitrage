# app.py

from flask import Flask, render_template, jsonify
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import time

app = Flask(__name__)

# Function to fetch token prices from the provided API response
def get_token_prices(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for any HTTP error

        # Parse the JSON response
        data = response.json()

        # Check if the API response contains the expected data structure
        if 'pairs' not in data or len(data['pairs']) == 0:
            raise ValueError("Unexpected API response format")

        # Extract token prices
        token_price_usd = float(data['pairs'][0]['priceUsd'])
        return token_price_usd

    except Exception as e:
        print(f"Error fetching token prices: {e}")
        return None

# Function to send email notification
def send_email(sender_email, receiver_email, password, subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.fastmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

# Function to periodically check price differences and send emails
def check_and_send_emails():
    while True:
        # API URLs for predefined tokens
        drb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd2d6690ca1575777e385ccfb59f2d346fe16aedc"
        drd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0xaba1ea940ba57aaeb8a2fd2891ad7cd0ea6cc3ec"
        dbrd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x98dc0d054d89ca6dfa591f9d5a46646181acf564"
        dbrb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xc1bf9be5070c2124070824b59f483835e971eb66"
        dbotd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x8a30d9d40b7fff6d601ce40bcde489d9467361d8"
        dbotb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd7baabd9310b8b5457f18847c512e25d4492b406"

        # Fetch token prices
        drb_price_usd = get_token_prices(drb_api_url)
        drd_price_usd = get_token_prices(drd_api_url)
        dbrd_price_usd = get_token_prices(dbrd_api_url)
        dbrb_price_usd = get_token_prices(dbrb_api_url)
        dbotd_price_usd = get_token_prices(dbotd_api_url)
        dbotb_price_usd = get_token_prices(dbotb_api_url)

        # Calculate price differences
        price_difference_dr = (100 * (drd_price_usd - drb_price_usd) / drb_price_usd)
        price_difference_dbr = (100 * (dbrd_price_usd - dbrb_price_usd) / dbrb_price_usd)
        price_difference_dbot = (100 * (dbotd_price_usd - dbotb_price_usd) / dbotb_price_usd)

        # Email notification setup
        sender_email = "arbdegen@fastmail.com"
        receiver_email = "serdar.basturk.52@gmail.com"
        password = "qqc7cwudhrxdjarz"
        subject = "Price Difference Notification"

        # Send email if price difference exceeds 5%
        if price_difference_dr > 5:
            body = f"Price difference (DR) is more than 5%: {price_difference_dr:.2f}%"
            send_email(sender_email, receiver_email, password, subject, body)

        if price_difference_dbr > 5:
            body = f"Price difference (DBR) is more than 5%: {price_difference_dbr:.2f}%"
            send_email(sender_email, receiver_email, password, subject, body)

        if price_difference_dbot > 5:
            body = f"Price difference (DBOT) is more than 5%: {price_difference_dbot:.2f}%"
            send_email(sender_email, receiver_email, password, subject, body)

        # Sleep for 5 minutes before checking again
        time.sleep(5 * 60)

# Start a new thread to periodically check price differences and send emails
email_thread = threading.Thread(target=check_and_send_emails)
email_thread.start()

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to return price differences as JSON
@app.route('/price_differences')
# Route to return price differences as JSON
@app.route('/price_differences')
def price_differences():
    # API URLs for predefined tokens
    drb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd2d6690ca1575777e385ccfb59f2d346fe16aedc"
    drd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0xaba1ea940ba57aaeb8a2fd2891ad7cd0ea6cc3ec"
    dbrd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x98dc0d054d89ca6dfa591f9d5a46646181acf564"
    dbrb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xc1bf9be5070c2124070824b59f483835e971eb66"
    dbotd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x8a30d9d40b7fff6d601ce40bcde489d9467361d8"
    dbotb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd7baabd9310b8b5457f18847c512e25d4492b406"

    # Fetch token prices
    drb_price_usd = get_token_prices(drb_api_url)
    drd_price_usd = get_token_prices(drd_api_url)
    dbrd_price_usd = get_token_prices(dbrd_api_url)
    dbrb_price_usd = get_token_prices(dbrb_api_url)
    dbotd_price_usd = get_token_prices(dbotd_api_url)
    dbotb_price_usd = get_token_prices(dbotb_api_url)

    # Calculate price differences
    price_difference_dr = (100 * (drd_price_usd - drb_price_usd) / drb_price_usd)
    price_difference_dbr = (100 * (dbrd_price_usd - dbrb_price_usd) / dbrb_price_usd)
    price_difference_dbot = (100 * (dbotd_price_usd - dbotb_price_usd) / dbotb_price_usd)

    # Construct JSON response with actual price differences
    price_differences_data = {
        'dr': price_difference_dr,
        'dbr': price_difference_dbr,
        'dbot': price_difference_dbot
    }

    return jsonify(price_differences_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
