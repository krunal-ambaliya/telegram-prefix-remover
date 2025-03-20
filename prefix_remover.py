from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Replace with your bot's API token
TOKEN = "7962967790:AAGaR2P3SK_EyZ-NuypMA9pIu0tDiynCRy8"

async def modify_message(update: Update, context: CallbackContext):
    """Modify messages in the channel by replacing the prefix."""
    if update.channel_post:
        # Handle text messages
        if update.channel_post.text and update.channel_post.text.startswith("@ASKOREANDRAMA"):
            new_message = update.channel_post.text.replace("@ASKOREANDRAMA", "@infinite_backup", 1)
            await context.bot.edit_message_text(
                chat_id=update.channel_post.chat_id,
                message_id=update.channel_post.message_id,
                text=new_message
            )

        # Handle media messages with captions
        elif update.channel_post.caption and update.channel_post.caption.startswith("@ASKOREANDRAMA"):
            new_caption = update.channel_post.caption.replace("@ASKOREANDRAMA", "@infinite_backup", 1)
            await context.bot.edit_message_caption(
                chat_id=update.channel_post.chat_id,
                message_id=update.channel_post.message_id,
                caption=new_caption
            )

def main():
    app = Application.builder().token(TOKEN).build()

    # Handle text messages
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, modify_message))

    # Handle media messages (photos, videos, documents) with captions
    app.add_handler(MessageHandler(filters.ATTACHMENT & filters.ChatType.CHANNEL, modify_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()