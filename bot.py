import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable (secure!)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

# Dictionary to store user data (in production, use a database)
user_data = {}

# -------------------- COMMAND HANDLERS --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
👋 Hello {user.first_name}!

I'm @john_doe_123bot - Your multifunctional assistant!
I can help you with various tasks.

🤖 Available Commands:
/start - Show this welcome message
/help - Show available commands
/echo <text> - Repeat what you say
/wordcount <text> - Count words and characters
/convert <format> - Convert files (coming soon)
/generate - AI image generation (coming soon)
/shorten <url> - Shorten URLs

📌 Click the buttons below to try some features!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("📝 Word Counter", callback_data='wordcounter'),
            InlineKeyboardButton("🔗 URL Shortener", callback_data='shortener')
        ],
        [
            InlineKeyboardButton("🖼️ Image Converter", callback_data='converter'),
            InlineKeyboardButton("✨ Image Generator", callback_data='generator')
        ],
        [
            InlineKeyboardButton("📊 Help", callback_data='help'),
            InlineKeyboardButton("ℹ️ About", callback_data='about')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    help_text = """
🤖 **@john_doe_123bot Help**

Here are all the things I can do:

**📝 Text Tools**
• `/wordcount <your text>` - Count words, characters, and more
• `/echo <text>` - Make me repeat after you

**🔗 URL Tools**
• `/shorten <url>` - Shorten long URLs

**🖼️ Image Tools** (Coming Soon)
• `/convert <image>` - Convert images to different formats
• `/generate <prompt>` - Generate AI images from text

**ℹ️ General**
• `/start` - Show welcome message
• `/help` - Show this help menu
• `/about` - About this bot

💡 **Quick Tips:**
• Click the buttons below messages for quick actions
• All processing is done securely
• Your data is private and not stored

Need more help? Contact @your_support_username
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send about information."""
    about_text = """
🤖 **About @john_doe_123bot**

**Version:** 1.0.0
**Created by:** Your Name
**Purpose:** A multifunctional Telegram assistant

**🛠 Features:**
• Word Counter
• URL Shortener
• Image Converter (Coming Soon)
• AI Image Generator (Coming Soon)

**🔧 Tech Stack:**
• Python 3.9+
• python-telegram-bot v20+
• Railway for hosting
• GitHub for version control

**📚 Resources:**
• Source Code: [GitHub](https://github.com/yourusername/telegram-bot)
• Report Issues: [Issues](https://github.com/yourusername/telegram-bot/issues)

Made with ❤️ using Python
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    if context.args:
        text_to_echo = ' '.join(context.args)
        await update.message.reply_text(f"🔊 Echo: {text_to_echo}")
    else:
        await update.message.reply_text("ℹ️ Please provide text to echo. Example: /echo Hello World!")

async def wordcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count words, characters, and more."""
    if not context.args:
        await update.message.reply_text("ℹ️ Please provide text to count. Example: /wordcount Hello world!")
        return
    
    text = ' '.join(context.args)
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_no_space = len(text.replace(' ', ''))
    sentence_count = len(text.split('.')) - 1 + len(text.split('!')) - 1 + len(text.split('?')) - 1
    
    stats = f"""
📊 **Word Count Statistics**

**Words:** {word_count}
**Characters (with spaces):** {char_count}
**Characters (without spaces):** {char_no_space}
**Sentences:** {sentence_count}
**Average word length:** {char_no_space/word_count:.1f} characters

📝 Your text:
_{text[:100]}{'...' if len(text) > 100 else ''}_
"""
    await update.message.reply_text(stats, parse_mode='Markdown')

async def shorten_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shorten a URL."""
    if not context.args:
        await update.message.reply_text("ℹ️ Please provide a URL to shorten. Example: /shorten https://example.com")
        return
    
    url = context.args[0]
    
    # Simple URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # For demonstration, we'll just return a shortened format
    # In production, you'd use an API like TinyURL or Bitly
    short_url = f"https://short.link/{hash(url) % 1000000:06d}"
    
    response = f"""
🔗 **URL Shortened**

**Original:** {url}
**Shortened:** {short_url}

📊 Click count: 0
⏰ Created: Just now
"""
    await update.message.reply_text(response, parse_mode='Markdown')

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "❌ I don't understand that command.\n"
        "Type /help to see available commands."
    )

# -------------------- CALLBACK QUERY HANDLERS --------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    responses = {
        'wordcounter': "📝 **Word Counter**\n\nUse /wordcount <your text>\nExample: /wordcount Hello world!",
        'shortener': "🔗 **URL Shortener**\n\nUse /shorten <url>\nExample: /shorten https://example.com",
        'converter': "🖼️ **Image Converter**\n\nComing soon! Send me an image and I'll convert it.",
        'generator': "✨ **AI Image Generator**\n\nComing soon! Describe an image and I'll generate it.",
        'help': "📊 **Help**\n\nType /help to see all commands.",
        'about': "ℹ️ **About**\n\nType /about to learn more about me."
    }
    
    response = responses.get(callback_data, "🤔 I'm not sure what you want!")
    await query.edit_message_text(response, parse_mode='Markdown')

# -------------------- MAIN FUNCTION --------------------

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("wordcount", wordcount))
    application.add_handler(CommandHandler("shorten", shorten_url))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add handler for unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown))
    
    # Start the Bot
    print("🤖 Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
