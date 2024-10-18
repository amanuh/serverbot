from pyrogram import Client, filters
import requests


# Replace these with your credentials
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '8005696768:AAHsL6SGht0M97Iuwd2vKKFIT06CBUUW39E'



# Initialize Pyrogram client
app = Client("minecraft_server_checker")



@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("Alla Hu Akabar☝️☝️")

@app.on_message(filters.command("check"))
async def check_minecraft_server(client, message):
    server_ip = "istanbull.falixsrv.me"  # Replace with your server IP or domain
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
            result_message = "❌ **The server is offline.**"

    except Exception as e:
        result_message = "An error occurred while checking the server status."
        print(e)

    # Edit the loading message with the result
    await loading_message.edit_text(result_message)

app.run()
