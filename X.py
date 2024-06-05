import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# "X" API credentials
x_api_key = 'fkBupsLbFeqtYMdvuEipIaWO1'
x_api_secret = 'ThMny5j93d5wMUPF1u8aq5HPcBvAxU6pIvUwd7WFvPN6FMDT9s'

# Twilio credentials
account_sid = 'AC346f4c5b14647be96ed8594e773ab163'
auth_token = '6127ff6dc74ecb1405cdc39ffbb20515'
twilio_number = '+12182178297'
your_number = '+212684455049'

# Twilio client
client = Client(account_sid, auth_token)

# Function to send SMS
def send_sms(message):
    client.messages.create(
        to=your_number,
        from_=twilio_number,
        body=message
    )

# Monitor "X" for new updates from a specific page
def monitor_x_service():
    # Make API request to "X" to check for new updates
    headers = {
        'X-API-Key': x_api_key,
        'X-API-Secret': x_api_secret
    }
    
    response = requests.get('https://x.com/1337FIL', headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        latest_post = soup.find('div', class_='post')  # Assuming posts are in a <div> with class 'post'
        
        # Extract the title of the post
        post_title = latest_post.find('h2').text.strip() if latest_post else None
        
        # Check if the latest post title is different from the previous one
        try:
            with open('previous_post.txt', 'r+') as file:
                previous_post = file.read()
                if post_title and post_title != previous_post:
                    # Update the previous post title in the file
                    file.seek(0)
                    file.truncate()
                    file.write(post_title)
                    
                    # Send SMS notification with post title
                    send_sms(f'New post on "X": {post_title}')
        except FileNotFoundError:
            # Create the file if it doesn't exist and write the initial post title
            with open('previous_post.txt', 'w') as file:
                file.write(post_title)
                if post_title:
                    send_sms(f'Initial post title saved for monitoring: {post_title}')

# Example usage
monitor_x_service()
