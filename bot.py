from pyrogram import Client, filters
import aiohttp

# Directly provide your credentials
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '8005696768:AAHsL6SGht0M97Iuwd2vKKFIT06CBUUW39E'

# Initialize Pyrogram client with bot token
app = Client("minecraft_server_checker", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("☝️☝️ Alla Hu Akabar")


@app.on_message(filters.command("check"))
async def check_minecraft_server(client, message):
    server_ip ="istanbull.falixsrv.me"  # Replace with your server IP or domain
    api_url = f"https://eu.mc-api.net/v3/server/ping/{server_ip}"

    # Send a loading message
    loading_message = await message.reply("Checking server status...")

    try:
        # Use aiohttp for asynchronous requests
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()

        if data.get("online"):
            player_count = data.get("players", {}).get("online", 0)
            max_players = data.get("players", {}).get("max", 0 )        
            result_message = (f"✅ **The server is online!**\n"
                              f"Version:Fabric Java 1.21 \n"
                              f"Players: {player_count}/{max_players}")

        elif data.get("offline"):
            result_message = " Serve is **offline** go to falixnodes.net/server/console to start the server"        
        else:
            result_message = "❌ **The server is offline.**"

    except Exception as e:
        result_message = "An error occurred while checking the server status."
        print(f"Error: {e}")

    # Edit the loading message with the result
    await loading_message.edit_text(result_message)

# Start the Pyrogram client
if __name__ == "__main__":
    app.run()
