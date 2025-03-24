from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_ADDRESS")
EMAIL_PASS = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/subscribe', method=['POST'])
def subscribe():
    subscriber_email = request.form.get('email')

    if not subscriber_email:
        flash("Please enter a valid email address.", "danger")
        return redirect(url_for('home'))

    # Email Content
    message = EmailMessage()
    message['Subject'] = "🎉 Welcome to JJ Taiyaki's Newsletter!"
    message['From'] = EMAIL_USER
    message['To'] = subscriber_email
    message.set_content(f"""
        Hi there,
        
        Thank you for subscribing to JJ Taiyaki's Newsletter!
        Stay tuned for exciting offers, delicious new treats, and more.

        See you soon at JJ Taiyaki!
        
        - JJ Taiyaki Team 🍡
    """)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(message)

        flash("🎉 Thank you for subscribing! Check your inbox.", "success")
    except Exception as e:
        print(f"Error sending email: {e}")
        flash("❌ Oops! Something went wrong. Try again later.", "danger")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
