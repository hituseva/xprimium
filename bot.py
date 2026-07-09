import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

CHANNEL_LINK = "https://t.me/+1ZCPS42UaNtlYjM1"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Payment complete karke screenshot bhejiye."
    )

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{user_id}")
        ]
    ])

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"Payment Screenshot\nUser ID: {user_id}",
        reply_markup=keyboard
    )

    await update.message.reply_text(
        "Screenshot receive ho gaya. Verification ka wait karein."
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment verified.\n\nChannel Link:\n{CHANNEL_LINK}"
        )
        await query.edit_message_caption(
            caption=query.message.caption + "\n\nAPPROVED"
        )

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment verify nahi ho paya. Kripya dubara screenshot bhejiye."
        )
        await query.edit_message_caption(
            caption=query.message.caption + "\n\nREJECTED"
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()
