# Taipei Bus Tracker

A Python script to track arrival times for specific Taipei bus stops using Selenium and send notifications to Telegram.

## Features

- Scrapes real-time arrival info from the Taipei City Traffic Real-time Information website.
- Runs in headless Chrome (background mode).
- Extracts specific stops for Go/Return routes.
- Sends formatted arrival times to a Telegram Chat.

## Prerequisites

- Python 3
- Google Chrome
- ChromeDriver (installed at `/usr/bin/chromedriver`)
- Selenium (`pip install selenium`)

## Usage

### 1. Set Environment Variables

You must provide your Telegram Bot Token and Chat ID as environment variables to enable notifications.

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### 2. Run the Script

```bash
python3 bus3.py
```

## Security Note

**Do not commit real API keys or tokens to GitHub.**
Required keys are read from environment variables to keep your code secure.

## GitHub Actions Setup

You can run this script automatically for free using GitHub Actions.

1.  Push this `bus` folder to a GitHub repository.
2.  Go to your repository **Settings** -> **Secrets and variables** -> **Actions**.
3.  Click **New repository secret**.
4.  Add the following secrets:
    *   Name: `TELEGRAM_BOT_TOKEN`, Value: (Your Bot Token)
    *   Name: `TELEGRAM_CHAT_ID`, Value: (Your Chat ID)
5.  The script will run automatically every day at 16:00 Taipei Time. You can also manually trigger it from the **Actions** tab.
