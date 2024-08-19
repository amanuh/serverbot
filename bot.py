from pyrogram import Client, filters
import requests


# Replace these with your credentials
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '6404091803:AAF4eI1cYt2BMxeRr_ZFqAJkElTGU11wao4'



# Initialize Pyrogram client
app = Client("minecraft_server_checker")



@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("Bot is Online")

@app.on_message(filters.command("check"))
async def check_minecraft_server(client, message):
    server_ip = "Toman03.aternos.me"  # Replace with your server IP or domain
    url = f"https://api.mcsrvstat.us/2/{server_ip}"

    # Send a loading message
    loading_message = await message.reply("Checking server status...")

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("online"):
            player_count = data.get("players", {}).get("online", 0)
            result_message = f"✅ **The server is online with {player_count} players.**"
        else:
            result_message = "❌ **The server is offline.**\n\n🔥 *Use /serverstart to start the server!*"

    except Exception as e:
        result_message = "An error occurred while checking the server status."
        print(e)

    # Edit the loading message with the result
    await loading_message.edit_text(result_message)

# Register the start_server command from the commands module
@app.on_message(filters.command("serverstart"))
async def start_server(client, message):
   await message.reply_text("soory this cmd is not ready yet")

app.run()
