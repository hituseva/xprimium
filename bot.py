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
ADMIN_ID = 6967545299
CHANNEL_LINK = "https://t.me/+1ZCPS42UaNtlYjM1"

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
        "✅ Screenshot receive ho gaya.\nVerification ka wait karein."
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if ":" not in query.data:
        return

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment verified.\n\nChannel Link:\n{CHANNEL_LINK}"
        )

    elif action == "reject":
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment verify nahi ho paya.\nKripya screenshot dubara bhejiye."
        )
        
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        plan_select,
        pattern="^plan_"
    )
)

app.add_handler(
    CallbackQueryHandler(
        button_click,
        pattern="^(approve|reject):"
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        receive_photo
    )
)

app.run_polling()
