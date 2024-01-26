import os
import requests
import telebot
from dotenv import load_dotenv
from storer import add_user
# Load environment variables
load_dotenv()
TG_API_KEY = os.getenv('TG_API_KEY')
CMC_API_KEY = os.getenv('CMC_API_KEY')
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Get Bitcoin price function
def get_bitcoin_price():
    parameters = {
        'start':'1',
        'limit':'2',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise an exception for bad requests
        data = response.json()

        # Extract the Bitcoin price from the response
        bitcoin_price = data['data'][0]['quote']['USD']['price']

        return bitcoin_price

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def create_bot():
    bot = telebot.TeleBot(TG_API_KEY)

    @bot.message_handler(commands=['greet'])
    def greet(message):
        bot.reply_to(message, "Hey whats up?")

    @bot.message_handler(commands=['gn'])
    def gn(message):
        bot.reply_to(message, "Goodnight 🌙")

    @bot.message_handler(commands=['gm'])
    def a(message):
        bot.reply_to(message, "Good morning ☀️")

    @bot.message_handler(commands=['btc'])
    def btc(message):
        btc_price = get_bitcoin_price()
        
        if btc_price is None:
            btc_price = "error"
        else:
            btc_price = f"${round(btc_price, 2)}"

        bot.reply_to(message, btc_price)
    
    @bot.message_handler(commands=['send'])
    def send(message):
        # Extract the message text following the /send command
        msg_text = message.text.split(' ', 1)
        #get the user_id
        user_id = message.from_user.id
        #and first name
        first_name = message.from_user.first_name
        
        print(msg_text)
        if len(msg_text) > 1:
            user_message = msg_text[1:]
            print(user_message)
            bot.reply_to(message, user_message)
            bot.reply_to(message, f"Hello, {first_name}! Your user ID is {user_id}")
            add_user(user_id, first_name)
        else:
            bot.reply_to(message, "Please provide a message to send.")

    return bot