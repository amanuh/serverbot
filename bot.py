from pyrogram import Client, filters
import aiohttp
import json
import os
import logging
import time  


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Store your credentials securely (avoid hardcoding)
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '7840927612:AAEuphtFALZwxp6MwT36SQw_rQ0TSbKBHOk'

grp_id = -1002308237145 
server_ip = "istanbull.falixsrv.me"
api_url = f"https://api.mcsrvstat.us/3/{server_ip}"

# Initialize Pyrogram client with bot token
app = Client("minecraft_server_checker", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("Glory to the God !")
    

@app.on_message(filters.command("check") & filters.chat(grp_id))
async def check_minecraft_server(client, message):
    loading_message = await message.reply("Checking server status...")
    

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        ip_address = data.get("ip", "N/A")
        version = data.get("version", "Unknown")
        players = data.get("players", {})
        player_count = players.get("online", 0)
        max_players = players.get("max", 0)

        result_message = (f"**🖥️ Server Status:**\n"
                          f"**🌐 IP**: {ip_address}\n"
                          f"**🔄 Version**: {version}\n"
                          f"**👥 Players**: {player_count}/{max_players}")

        

    except Exception as e:
        result_message = "An error occurred while checking the server status."
        logging.error(f"Error while checking server status: {e}")

    await loading_message.edit_text(result_message)

@app.on_message(filters.command("players"))
async def get_players_list(client, message):
    loading_message = await message.reply("Fetching list of players...")
    

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        player_names = data.get("players", {}).get("list", [])
        if player_names:
            result_message = "**👥 Players currently online:**\n" + "\n".join(player_names)
        else:
            result_message = "No players are currently online."

       

    except Exception as e:
        result_message = "An error occurred while fetching the players list."
        logging.error(f"Error while fetching players list: {e}")

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

        file_path = "minecraft_server_status.txt"
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
    loading_message = await message.reply("Pinging the Minecraft Server...")
    

    start_time = time.time()  # Record the start time
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

        end_time = time.time()  # Record the end time
        ping_time = (end_time - start_time) * 1000  # Convert to milliseconds

        result_message = f"**🏓 Server Ping:** {ping_time:.2f} ms"
        

    except Exception as e:
        result_message = "An error occurred while pinging the server."
        logging.error(f"Error while pinging server: {e}")

    await loading_message.edit_text(result_message)



# Start the Pyrogram client
if __name__ == "__main__":
    logging.info("Starting the bot...")
    app.run()
    logging.info("Bot has been stopped.")
