🚀 Hello Devs!
I just released Agent-Bot — an open-source AI Telegram bot that makes working with images, videos, and documents super easy!
✨ What can Agent-Bot do?
Enhance and convert images in a snap
Clean and process audio and video files
Summarize PDFs and analyze JSON files
Chat with you using AI
...and much more!
🛠️ For Developers:
Agent-Bot is designed to be modular and beginner-friendly. Want to add your own service? You can! The code is organized so you can easily plug in new features for handling images, videos, documents, or anything else you dream up.
Whether you’re a user who wants a smart media assistant, or a developer looking to build and extend your own AI bot, Agent-Bot is for you.
👉 Try it out, star the repo, and feel free to contribute or suggest new features:

# agent-bot

A modular AI-powered Telegram agent bot built in Python, designed to handle a variety of user commands including PDF processing, document conversion, video-to-gif conversion, and more.

## Features

* **PDF Processing**: Extracts text and metadata from PDFs (docs\_conversion, process\_pdf\_handler). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* **Document Conversion**: Converts documents between various formats (docs\_conversion.py). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* **Video Handling**: Supports video processing tasks such as video-to-gif conversion (convert\_video\_handler, convert\_to\_gif\_handler). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* **Intent Detection**: Determines user intents for routing commands (intent\_detect). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* **Memory Storage**: Stores session or conversation memory for context-aware interactions (memory\_storage). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* **Custom Keyboards & Menus**: Provides interactive Telegram keyboard menus (keyboards, menu). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))

## Prerequisites

* Python 3.8 or higher ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
* A Telegram Bot API token (store in `.env`). ([github.com](https://github.com/Lucky-Kandpal/agent-bot))

## Installation

1. **Clone the repository**:

   ````bash
   git clone https://github.com/Lucky-Kandpal/agent-bot.git
   ``` ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
   ````
2. **Navigate to project directory**:

   ````bash
   cd agent-bot
   ``` ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
   ````
3. **Install dependencies**:

   ````bash
   pip install -r requirements.txt
   ``` ([github.com](https://github.com/Lucky-Kandpal/agent-bot))
   ````
4. **Create a `.env` file** based on `.env.example` and add your Telegram Bot token and other configs. ([github.com](https://github.com/Lucky-Kandpal/agent-bot))

## Configuration

* `.env`

  * `TELEGRAM_TOKEN`: Your Telegram Bot API token.
  * `LOG_LEVEL`: (optional) Logging level (default: INFO).
  * `OTHER_CONFIG`: Add other environment variables as needed. ([github.com](https://github.com/Lucky-Kandpal/agent-bot))

## Running the Bot

Execute the main application:

````bash
python app.py
``` ([raw.githubusercontent.com](https://raw.githubusercontent.com/Lucky-Kandpal/agent-bot/main/app.py))

## Project Structure

````

agent-bot/
├── api\_req/                 # API request utilities
├── bot/                     # Bot initializer and application runner
├── commands/                # Command definitions
├── handlers/                # Handler modules for different functionalities
├── intent\_detect/           # Intent detection logic
├── keyboards/               # Telegram keyboard layouts
├── memory\_storage/          # Memory storage backend
├── menu/                    # Menu configurations
├── convert\_to\_gif\_handler.py
├── convert\_video\_handler.py
├── docs\_conversion.py
├── process\_pdf\_handler.py
├── system\_prompt.py         # System prompt configurations
├── env\_config.py            # Environment config loader
├── app.py                   # Entry point
├── requirements.txt
└── .env.sample              # Sample environment file

```([github.com](https://github.com/Lucky-Kandpal/agent-bot))


