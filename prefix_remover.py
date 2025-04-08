import os
import psutil
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Auto-kill other running instances of this script
def kill_other_instances():
    current_pid = os.getpid()
    script_name = os.path.basename(__file__)

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (
                proc.info['pid'] != current_pid and
                proc.info['cmdline'] and
                script_name in proc.info['cmdline'] and
                "python" in proc.info['name'].lower()
            ):
                print(f"🔴 Terminating previous bot instance with PID {proc.info['pid']}")
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

kill_other_instances()

# ENV Token
TOKEN = os.getenv("BOT_TOKEN")

# Prefix map for replacements
prefix_map = {}  # Example: {'@ASKOREANDRAMA': '@infinite_backup'}

# 📌 Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your Prefix Replacer Bot. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available Commands:\n"
        "/add_prefix <old> <new> - Add a prefix replacement\n"
        "/remove_prefix <old> - Remove a prefix\n"
        "/list_prefix - Show all active prefix replacements"
    )

async def add_prefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /add_prefix <old> <new>")
        return
    old, new = context.args
    prefix_map[old] = new
    await update.message.reply_text(f"✅ Added prefix replacement: {old} → {new}")

async def remove_prefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove_prefix <old>")
        return
    old = context.args[0]
    if old in prefix_map:
        del prefix_map[old]
        await update.message.reply_text(f"🗑 Removed prefix replacement: {old}")
    else:
        await update.message.reply_text("❌ Prefix not found.")

async def list_prefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not prefix_map:
        await update.message.reply_text("📭 No prefix replacements set.")
    else:
        msg = "🔁 Active Prefix Replacements:\n"
        for k, v in prefix_map.items():
            msg += f"{k} → {v}\n"
        await update.message.reply_text(msg)

# 🧠 Message Modifier for Channels
async def modify_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        # Replace in text
        if update.channel_post.text:
            for old, new in prefix_map.items():
                if update.channel_post.text.startswith(old):
                    new_text = update.channel_post.text.replace(old, new, 1)
                    await context.bot.edit_message_text(
                        chat_id=update.channel_post.chat_id,
                        message_id=update.channel_post.message_id,
                        text=new_text
                    )
                    break

        # Replace in caption
        elif update.channel_post.caption:
            for old, new in prefix_map.items():
                if update.channel_post.caption.startswith(old):
                    new_caption = update.channel_post.caption.replace(old, new, 1)
                    await context.bot.edit_message_caption(
                        chat_id=update.channel_post.chat_id,
                        message_id=update.channel_post.message_id,
                        caption=new_caption
                    )
                    break

# 🚀 Main Bot Setup
def main():
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_prefix", add_prefix))
    app.add_handler(CommandHandler("remove_prefix", remove_prefix))
    app.add_handler(CommandHandler("list_prefix", list_prefix))

    # Register message handler for channel posts
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, modify_message))
    app.add_handler(MessageHandler(filters.ATTACHMENT & filters.ChatType.CHANNEL, modify_message))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
