from pyrogram import Client, filters
import aiohttp
import json
import os
import logging
import time
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

AFK_FILE = "afk_status.json"

# Start client
app = Client("minecraft_server_checker", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# AFK users dictionary
afk_users = {}
if os.path.exists(AFK_FILE):
    try:
        with open(AFK_FILE, "r") as f:
            afk_users = json.load(f)
    except json.JSONDecodeError:
        logging.error("AFK file corrupted. Starting fresh.")
        afk_users = {}

# Commands
@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("Bot is online and ready to assist!")

@app.on_message(filters.command("check") & filters.chat(grp_id))
async def check_minecraft_server(client, message):
    loading_message = await message.reply("Checking server status...")
    try:
        async with aiohttp.ClientSession() as session:
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

@app.on_message(filters.command("json") & filters.chat(grp_id))
async def get_json_response(client, message):
    loading_message = await message.reply("Fetching JSON response...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        file_path = "minecraft_server_status.json"
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        await client.send_document(message.chat.id, file_path, caption="Here is the JSON response.")
        logging.info(f"JSON response saved to {file_path} and sent to user.")
        os.remove(file_path)
    except Exception as e:
        result_message = "An error occurred while fetching the JSON response."
        logging.error(f"Error while fetching JSON response: {e}")
        await loading_message.edit_text(result_message)

@app.on_message(filters.command("ping"))
async def ping_server(client, message):
    loading_message = await message.reply("Pinging the Minecraft server...")
    start_time = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

        end_time = time.time()
        ping_time = (end_time - start_time) * 1000  # Convert to milliseconds
        result_message = f"**🏓 Bot Ping:** {ping_time:.2f} ms"
    except Exception as e:
        result_message = "An error occurred while pinging the server."
        logging.error(f"Error while pinging server: {e}")

    await loading_message.edit_text(result_message)

@app.on_message(filters.command(["afk"]))
async def afk_handler(client: Client, message: Message):
    reason = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    afk_users[message.from_user.id] = {"reason": reason}
    await message.reply("You are now AFK.")
    try:
        with open(AFK_FILE, "w") as f:
            json.dump(afk_users, f, indent=4)
    except Exception as e:
        logging.error(f"Error writing to AFK file: {e}")

@app.on_message(filters.text)
async def message_handler(client: Client, message: Message):
    if message.from_user.id in afk_users:
        del afk_users[message.from_user.id]
        try:
            with open(AFK_FILE, "w") as f:
                json.dump(afk_users, f, indent=4)
        except Exception as e:
            logging.error(f"Error writing to AFK file: {e}")
        await message.reply("Welcome back!")

@app.on_message(filters.mentioned | filters.reply)
async def mention_reply_handler(client: Client, message: Message):
    # Check if it's a reply
    if message.reply_to_message:
        afk_user = afk_users.get(message.reply_to_message.from_user.id)
        if afk_user:
            reason = afk_user["reason"] or "No reason given."
            user_name = message.reply_to_message.from_user.first_name
            await message.reply(f"The user {user_name} is AFK: {reason}")
            return

    # Check if it's a mention
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention" and entity.user:  # Handle direct user mentions
                afk_user = afk_users.get(entity.user.id)
                if afk_user:
                    reason = afk_user["reason"] or "No reason given."
                    user_name = entity.user.first_name
                    await message.reply(f"The user {user_name} is AFK: {reason}")
                    return
            elif entity.type == "mention":  # Handle username mentions
                username = message.text[entity.offset : entity.offset + entity.length].lstrip("@")
                try:
                    user = await client.get_users(username)
                    afk_user = afk_users.get(user.id)
                    if afk_user:
                        reason = afk_user["reason"] or "No reason given."
                        user_name = user.first_name
                        await message.reply(f"The user {user_name} is AFK: {reason}")
                        return
                except Exception as e:
                    # Log or handle errors (e.g., user not found)
                    print(f"Error fetching user: {e}")
                          

# Run the bot
if __name__ == "__main__":
    logging.info("Starting the bot...")
    app.run()
    logging.info("Bot has been stopped.")
