import asyncio
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import nest_asyncio

# Nest asyncio ni qo'llash
nest_asyncio.apply()

# OpenAI API kalitini kiriting
openai.api_key = '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'

# Tarjima funksiyasi
async def translate_text(text, target_language):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Translate the following text to {target_language}: {text}",
            max_tokens=60
        )
        translation = response.choices[0].text.strip()
        return translation
    except Exception as e:
        return f"Xato yuz berdi: {e}"

# /start komandasi
async def start(update: Update, context):
    await update.message.reply_text("Salom! Men tarjimon botman. Ingliz tilidan o'zbekchaga va o'zbek tilidan inglizchaga tarjima qilish uchun xabar yozing.")

# Tarjima qilish funksiyasi
async def translate(update: Update, context):
    text = update.message.text
    if text.isascii():  # Ingliz tilida
        dest_lang = 'Uzbek'
    else:  # O'zbek tilida
        dest_lang = 'English'
    
    translation = await translate_text(text, dest_lang)
    await update.message.reply_text(translation)

async def main():
    application = Application.builder().token("7400374470:AAF2TEh4qPeM12tmGQp03tpkdH8nNeYJdhA").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
