import telebot
import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

MAIL,GENDER,FNAME,MNAME, PHOTO, LOCATION, BIO = range(7)
bot = telebot.TeleBot("5801894058:AAHVsIs2ml3VdZWEXeuMvyKFIS3G_AZlCFI")
@bot.message_handler(commands=['start'])

def send_welcome(message):
    bot.reply_to(message, "Welcome! Type /register to register \nor /complain to file a complaint or\n /help for help.")

@bot.message_handler(commands=['register'])
def register_handler(message):
    bot.send_message(message.chat.id,"Enter your name:")
    bot.register_next_step_handler(message, handle_student_name)
def handle_student_name(message):
    bot.send_message(message.chat.id,"Enter your college mail ID")
    bot.register_next_step_handler(message, handle_student_mail)

def handle_student_mail(message):
    email = message.text.split()[-1]
    match = re.search(r"[a-zA-Z0-9._%+-]+@vvit\.[a-zA-Z]{2,}", email)
    if match:
       
        bot.send_message(message.chat.id, "You have been registered successfully! check your mail for further details")
    else:
        
        bot.send_message(message.chat.id, "Invalid email address. Please enter a valid  email address.")


@bot.message_handler(commands=['complain'])
def handle_complaint(message):
    bot.send_message(message.chat.id, "Are you a student of this college? (yes/no)")
    bot.register_next_step_handler(message, handle_student_response)

def handle_student_response(message):
    if message.text.lower() == "yes":
        bot.send_message(message.chat.id, "Please enter your complaint.")
        bot.register_next_step_handler(message, handle_complaint_text)
    elif message.text.lower() == "no":
        bot.send_message(message.chat.id, "Thank you for your interest, but only students can file complaints.")
    else:
        bot.send_message(message.chat.id, "Invalid response. Please enter 'yes' or 'no'.")
        bot.register_next_step_handler(message, handle_student_response)

def handle_complaint_text(message):
    complaint_text = message.text
    # process complaint
    bot.send_message(message.chat.id, " thank you .Your complaint has been received .Your complaint is: " + complaint_text )
    bot.send_message(message.chat.id, "Do you have a photo to send? (yes/no)")
    bot.register_next_step_handler(message, handle_photo_response,complaint_text)

def handle_photo_response(message,complaint_text):
    if message.text == "yes":
        bot.send_message(message.chat.id, "Please send a photo of the issue.")
        bot.register_next_step_handler(message, handle_photo,complaint_text)
    elif message.text == "no":
        bot.send_message(message.chat.id, "Thank you for your complaint, no photo was received.")
    else:
        bot.send_message(message.chat.id, "Invalid response. Please enter 'yes' or 'no'.(case sensitive)")
        bot.register_next_step_handler(message, handle_photo_response,complaint_text)
        
def handle_photo(message,complaint_text):
    if message.photo:
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        downloaded_file = bot.download_file(file.file_path)
        with open("issue.jpg", "wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id, "Complaint received: " + complaint_text + " and photo has been saved.")
    else:
        bot.send_message(message.chat.id, "No photo received. Please send a photo of the issue.")
        bot.register_next_step_handler(message, handle_photo,complaint_text)

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "For assistance, please visit our website https://www.vignannirula.org")


bot.polling()
