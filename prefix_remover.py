from telegram import Update
from telegram.ext import (
    Application, MessageHandler, CommandHandler,
    filters, CallbackContext
)
import os

TOKEN = os.getenv("BOT_TOKEN")

# Store prefix replacements
prefix_map = {}  # Example: { "@ASKOREANDRAMA": "@infinite_backup" }

async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome! I'm here to help manage your prefixes.")

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🛠 Available commands:\n"
        "/add_prefix <old_prefix> <new_prefix> - Add a prefix replacement.\n"
        "/remove_prefix <old_prefix> - Remove a prefix replacement.\n"
        "/list_prefix - Show all current prefix mappings."
    )

async def add_prefix(update: Update, context: CallbackContext):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /add_prefix <old_prefix> <new_prefix>")
        return

    old_prefix, new_prefix = context.args
    prefix_map[old_prefix] = new_prefix
    await update.message.reply_text(f"✅ Added prefix replacement:\n{old_prefix} ➝ {new_prefix}")

async def remove_prefix(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove_prefix <old_prefix>")
        return

    old_prefix = context.args[0]
    if old_prefix in prefix_map:
        del prefix_map[old_prefix]
        await update.message.reply_text(f"❌ Removed prefix replacement for: {old_prefix}")
    else:
        await update.message.reply_text("⚠️ That prefix doesn't exist.")

async def list_prefix(update: Update, context: CallbackContext):
    if not prefix_map:
        await update.message.reply_text("📭 No prefixes have been added yet.")
        return

    msg = "📌 Current prefix replacements:\n"
    for old, new in prefix_map.items():
        msg += f"{old} ➝ {new}\n"
    await update.message.reply_text(msg)

async def modify_message(update: Update, context: CallbackContext):
    """Modify messages in the channel by replacing the prefix."""
    if update.channel_post:
        # Handle text messages
        if update.channel_post.text:
            new_text = update.channel_post.text
            for old, new in prefix_map.items():
                if new_text.startswith(old):
                    new_text = new_text.replace(old, new, 1)
                    await context.bot.edit_message_text(
                        chat_id=update.channel_post.chat_id,
                        message_id=update.channel_post.message_id,
                        text=new_text
                    )
                    return

        # Handle media messages with captions
        elif update.channel_post.caption:
            for old, new in prefix_map.items():
                if old in update.channel_post.caption:
                    new_caption = update.channel_post.caption.replace(old, new, 1)
                    await context.bot.edit_message_caption(
                        chat_id=update.channel_post.chat_id,
                        message_id=update.channel_post.message_id,
                        caption=new_caption
                    )
                    break


def main():
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_prefix", add_prefix))
    app.add_handler(CommandHandler("remove_prefix", remove_prefix))
    app.add_handler(CommandHandler("list_prefix", list_prefix))

    # Modify messages in the channel
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, modify_message))
    app.add_handler(MessageHandler(filters.ATTACHMENT & filters.ChatType.CHANNEL, modify_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
