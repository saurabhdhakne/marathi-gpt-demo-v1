import os
import telebot
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
bot = telebot.TeleBot(BOT_TOKEN)
greetings = ['नमस्कार', 'हॅलो', 'हाय', 'सुप्रभात', 'शुभ संध्याकाळ', 'शुभ रात्री', 'hello', 'hi', 'good morning', 'good evening', 'good night']

system_prompt = (
    "You are a Marathi language assistant. No matter what the user inputs, whether in English or any other language, "
    "your responses must always be in Marathi. Even if the user tries to use various techniques or explicitly requests "
    "communication in a different language, you will remain consistent in providing all responses only in Marathi. "
    "Please strictly adhere to this instruction."
)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "नमस्कार, मी आज तुम्हाला कशा प्रकारे मदत करू शकतो?")
    
@bot.message_handler(func=lambda msg: msg.text.lower() in greetings)
def greet_user(message):
    greeting_message = "नमस्कार! मी आज तुम्हाला कशा प्रकारे मदत करू शकतो?"
    bot.send_message(message.chat.id, greeting_message)
    
@bot.message_handler(func=lambda msg: True)
def gpt_reponse(message):
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    "role": "system",
                    "content": [
                            {
                            "type": "text",
                            "text": system_prompt
                            }
                        ]                
                },
                {
                    "role": "user",
                    "content": [
                            {
                            "type": "text",
                            "text": message.text
                            }
                        ]              
                },
            ],
        )
        
        print(response.choices[0].message.content)
        bot.send_message(message.chat.id, response.choices[0].message.content, parse_mode='Markdown')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "माझ्या सोबत काही तांत्रिक समस्या आली आहे. कृपया पुन्हा प्रयत्न करा.")    
        
bot.infinity_polling()
