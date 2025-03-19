from common.repo.repository import DatabaseRepository
from models import database
from cruds import crud_credentials, crud_users
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    Application,
    CommandHandler,
    ContextTypes,
)
from dependencies import TELEGRAM_TOKEN, serializer, get_repo
import logging

logging.basicConfig(level=logging.INFO)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot started! Ready to handle user approvals.")


def confirm_user(token: str):
    try:
        login = serializer.loads(token)
    except Exception:
        raise Exception("The token is invalid or has been expired")

    session = database.SessionLocal()
    repo = DatabaseRepository(session)
    user_id = crud_credentials.get_user_id_by_login(repo, login)
    crud_users.make_user_root(repo, user_id)


async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Approving the user...")
    query = update.callback_query
    token = query.data

    try:
        response = confirm_user(token)
        await query.message.edit_text("✅ User has been approved successfully!")
    except Exception as e:
        logging.error(e)
        await query.message.edit_text(f"❌ Error occurred: please, try again")


async def start_bot():
    return
    try:
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(approve_user))

        logging.info("Starting bot process...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
