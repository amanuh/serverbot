from pyrogram import Client, filters
import aiohttp
import logging
import asyncio
from pyrogram.types import Message

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Bot credentials
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '7840927612:AAEuphtFALZwxp6MwT36SQw_rQ0TSbKBHOk'

# Server details
grp_id = -1002308237145
server_ip = "srv20011.host2play.gratis"
api_url = f"https://api.mcsrvstat.us/3/{server_ip}"

# Global aiohttp session
session = None

# Initialize the Pyrogram Client
app = Client("minecraft_server_checker", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Commands
@app.on_message(filters.command("start"))
async def bot_online(client, message: Message):
    await message.reply_text("Glory to God!")

@app.on_message(filters.command("check") & filters.chat(grp_id))
async def check_minecraft_server(client, message: Message):
    loading_message = await message.reply("Checking server status...")
    try:
        async with session.get(api_url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

            data = await response.json()

        # Extract server details
        ip_address = data.get("ip", "N/A")
        version = data.get("version", "Unknown")
        players = data.get("players", {})
        player_count = players.get("online", 0)
        max_players = players.get("max", 0)

        result_message = (
            f"**🖥️ Server Status:**\n"
            f"**🌐 Server Address**: `{server_ip}`\n"
            f"**🔄 Version**: {version}\n"
            f"**👥 Players**: {player_count}/{max_players}\n"
            f"[Renew Server](https://host2play.gratis/server/renew?i=1b131c4a-b306-4826-95fe-b2e9469aaa66), if stopped\n"
        )
    except Exception as e:
        result_message = "An error occurred while checking the server status."
        logging.error(f"Error while checking server status: {e}")

    await loading_message.edit_text(result_message)


# Main function to handle startup and shutdown
async def main():
    global session
    try:
        logging.info("Initializing aiohttp session...")
        session = aiohttp.ClientSession()  # Initialize aiohttp session

        logging.info("Starting Pyrogram client...")
        await app.start()  # Start the Pyrogram client

        logging.info("Bot is running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()  # Keep running until interrupted
    except (KeyboardInterrupt, SystemExit):
        logging.info("Shutdown signal received.")
    finally:
        logging.info("Stopping Pyrogram client...")
        await app.stop()  # Stop the Pyrogram client

        if session:
            logging.info("Closing aiohttp session...")
            await session.close()  # Cleanup aiohttp session
        logging.info("Bot has been shut down.")

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
