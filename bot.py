from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

ADMIN_ID = 6967545299

async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

app = Application.builder().token("BOT_TOKEN").build()
app.add_handler(MessageHandler(filters.ALL, receive))
app.run_polling()
