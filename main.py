import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification
import json

# Constants
API_KEY = 'your_openweathermap_api_key'
CITY = 'your_city'
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'
RECIPIENT_EMAIL = 'recipient_email@example.com'

# Fetch weather data
def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

# Check for severe weather
def check_severe_weather(data):
    if 'weather' in data:
        weather_description = data['weather'][0]['description']
        if 'storm' in weather_description or 'rain' in weather_description:
            return True
    return False

# Send email alert
def send_email_alert(subject, body, to_email, from_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

# Send desktop notification
def send_desktop_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# Main function
def main():
    weather_data = get_weather_data(API_KEY, CITY)
    
    if check_severe_weather(weather_data):
        alert_message = f"Severe weather alert in {CITY}. Weather details: {weather_data['weather'][0]['description']}"
        
        # Send email alert
        send_email_alert("Weather Alert", alert_message, RECIPIENT_EMAIL, EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send desktop notification
        send_desktop_notification("Weather Alert", alert_message)
    else:
        print("Weather conditions are normal.")

if __name__ == "__main__":
    main()
