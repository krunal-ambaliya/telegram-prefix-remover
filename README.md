# 🔁 Telegram Prefix Replacement Bot

This is a Telegram bot designed to **automatically replace specific prefixes** in messages posted in **Telegram channels**. It’s perfect for channel admins who want to automate text or caption edits like replacing `@OLDCHANNEL` with `@NEWCHANNEL`.

---

## 🚀 Features

- 📌 Replace prefixes in messages and media captions automatically
- ➕ Add or remove custom prefix mappings on the fly
- 📋 List all active replacements
- 💬 Modify both text and media captions in channel posts

---

## 🧪 Example Use Case

If your channel forwards content from another with a prefix like `@AskoreanDrama` and you want to automatically change it to your backup handle `@infinite_backup`, just use:

/add_prefix @AskoreanDrama @infinite_backup

yaml
Copy
Edit

The bot will replace the prefix in future messages posted in the channel.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-prefix-bot.git
cd telegram-prefix-bot
```
## 2. Install dependencies
Make sure Python 3.7+ is installed.

```
pip install python-telegram-bot==20.3
```
## 3. Set your Bot Token
Create a .env file or set the environment variable in your system:

```
BOT_TOKEN=your_telegram_bot_token_here
```
Or temporarily in your terminal:
```
export BOT_TOKEN=your_telegram_bot_token_here
```
- 🔐 You can get the bot token from [@BotFather](https://telegram.me/BotFather).

## 4. Run the Bot

```
python3 bot.py
```
> ✅ The bot should print 🤖 Bot is running... when successfully launched.


## 📚 Available Commands

| Command                      | Description                               |
|-----------------------------|-------------------------------------------|
| `/start`                    | Greet the user                            |
| `/help`                     | Show help and available commands          |
| `/add_prefix <old> <new>`   | Add a new prefix replacement              |
| `/remove_prefix <old>`      | Remove an existing prefix replacement     |
| `/list_prefix`              | Show all current prefix mappings          |

---

## 🔒 Permissions Required

To work properly in a channel:

- Add the bot as an **admin** in your channel.
- Grant the bot the **Edit messages** permission.

---

## 💬 Message Handling

The bot will:

- Automatically **edit text messages** in channels if they begin with a registered old prefix.
- Replace **captions** in media posts** that contain the old prefix.

---

## 👤 Author & Contact

Made with ❤️ by **Krunal**

📬 **Telegram**: [@krues](https://t.me/krues)

For help, feedback, or more Telegram bot projects, feel free to reach out!
