import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.errors import FloodWaitError

API_ID = 'PLACEHOLDER_API_ID'
API_HASH = 'PLACEHOLDER_API_HASH'
BOT_TOKEN = 'PLACEHOLDER_BOT_TOKEN'

# Directory to save the PDF. Can be overridden by an environment variable.
DOWNLOAD_DIR = os.environ.get('DOWNLOAD_DIR', 'outputs/')

# Ensure essential credentials are provided
if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set either in Colab secrets or as environment variables.")

number = 1

# Define a dictionary to store your message link lists
MESSAGE_LINKS = {
    1: [
        'https://t.me/cengage_personal/335',
        'https://t.me/cengage_personal/336',
        'https://t.me/cengage_personal/337'
    ]
}

# Create the Telegram Client instance (don't call .start() yet)
client = TelegramClient('session_name', API_ID, API_HASH)

async def download_pdfs_from_links(telegram_client, links):
    # Ensure the download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for link in links:
        try:
            # Parse the message link
            parts = link.split('/')
            channel_username = parts[-2]  # Extract channel username
            message_id = int(parts[-1])  # Extract message ID

            # Bots cannot access private channels using the 't.me/c/' link style format
            if channel_username == 'c':
                print(f"Skipping link {link}: Bots cannot access private channel links ('/c/') directly.")
                continue

            # Get the message by ID using the passed client instance
            message = await telegram_client.get_messages(channel_username, ids=message_id)

            # Check if the message has a document and if it's a PDF
            if message and message.document and message.document.mime_type == 'application/pdf':
                # Download the PDF
                file_path = await message.download_media(file=DOWNLOAD_DIR)
                print(f"Downloaded: {file_path}")
            else:
                print(f"No PDF found in message: {link}")

        except FloodWaitError as e:
            print(f"FloodWaitError: Need to wait for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
            print("Retrying...")

        except Exception as e:
            print(f"Failed to process link {link}: {e}")

async def main():
    # Start the client with the bot token
    await client.start(bot_token=BOT_TOKEN)

    # Call the async download function, passing the client instance
    await download_pdfs_from_links(client, MESSAGE_LINKS.get(number))

    # Disconnect the client when done
    await client.disconnect()

# Run the main async function when executed directly
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(0)
