# Telegram Booking Bot

Bot for booking services via Telegram (aiogram 3 + SQLAlchemy).

## Features

- Choose a service (haircut, consultation, manicure)
- Leave name and phone
- Booking is saved to the database
- Admin gets a notification with booking details
- Users can view their bookings

## Tech stack

- Python 3.11+
- aiogram 3
- SQLAlchemy 2 (async) + aiosqlite
- SQLite

## Setup

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt



## Don't forget to create an .env file and add next things
BOT_TOKEN=your_token
ADMIN_ID=your_telegram_id