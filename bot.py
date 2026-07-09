import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("₹10 - 1 Day", callback_data="plan_1"),
            InlineKeyboardButton("₹50 - 30 Days", callback_data="plan_30")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=open("qr.jpg", "rb"),
        caption="UPI ID: rzphitusolanki691055.rzp@ypbiz\n\nPayment karke plan select karein.",
        reply_markup=reply_markup
    )

async def plan_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "plan_1":
        await query.message.reply_text(
            "₹10 (1 Day) plan selected.\nPayment screenshot bhejiye."
        )

    elif query.data == "plan_30":
        await query.message.reply_text(
            "₹50 (30 Days) plan selected.\nPayment screenshot bhejiye."
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(plan_select))

app.run_polling()
