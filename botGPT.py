import logging
from dotenv import load_dotenv
import os
import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()  # .env faylidagi o‘zgaruvchilarni yuklaydi

# O‘zgaruvchilarni olish
token = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
user_id = int(os.getenv("USER_KEY"))

if token is None or openai.api_key is None or user_id is None:
    raise ValueError("Kerakli o‘zgaruvchilar .env faylida mavjud emas.")

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True)
def get_response(message):
  if int(message.chat.id) != user_id:
    bot.send_message(message.chat.id, "This bot is not for public but private use only.")
  else:
    response = ""
    if message.text.startswith(">>>"):
      # Codex API for code completion
      response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=f'```\n{message.text[3:]}\n```',
        temperature=0,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n", ">>>"],
      )
    else:
      # GPT API for text completion
      if "code" in message.text.lower() or "python" in message.text.lower():
        # Codex API for code-related questions
        response = openai.Completion.create(
          engine="code-davinci-002",
          prompt=f'"""\n{message.text}\n"""',
          temperature=0,
          max_tokens=4000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=['"""'],
        )
      else:
        # GPT API for non-code-related questions
        response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=f'"""\n{message.text}\n"""',
          temperature=0,
          max_tokens=2000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
          stop=['"""'],
        )

    bot.send_message(message.chat.id, f'{response["choices"][0]["text"]}', parse_mode="None")

bot.infinity_polling()
