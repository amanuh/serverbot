from pyrogram import Client, filters
import aiohttp
import json
import os  # Import os to handle file paths
from ping import ping_command

# Store your credentials securely (avoid hardcoding)
api_id = '12997033'
api_hash = '31ee7eb1bf2139d96a1147f3553e0364'
bot_token = '7840927612:AAEuphtFALZwxp6MwT36SQw_rQ0TSbKBHOk'

server_ip = "istanbull.falixsrv.me"
api_url = f"https://api.mcsrvstat.us/3/{server_ip}"

# Initialize Pyrogram client with bot token
app = Client("minecraft_server_checker", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def bot_online(client, message):
    await message.reply_text("Glory to the God !")

@app.on_message(filters.command("check"))
async def check_minecraft_server(client, message):
    # Send a loading message
    loading_message = await message.reply("Checking server status...")

    try:
        # Use aiohttp for asynchronous requests
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        # Extract specific variables from the JSON response, with default values
        ip_address = data.get("ip", "N/A")
        version = data.get("version", "Unknown")
        players = data.get("players", {})
        player_count = players.get("online", 0)
        max_players = players.get("max", 0)

        # Create the response message with the selected variables
        result_message = (f"**🖥️ Server Status:**\n"
                          f"**🌐 IP**: {ip_address}\n"
                          f"**🔄 Version**: {version}\n"
                          f"**👥 Players**: {player_count}/{max_players}")

    except Exception as e:
        result_message = "An error occurred while checking the server status."
        print(f"Error: {e}")  # Log error for debugging purposes

    # Edit the loading message with the selected variables or error message
    await loading_message.edit_text(result_message)

@app.on_message(filters.command("players"))
async def get_players_list(client, message):

    # Send a loading message
    loading_message = await message.reply("Fetching list of players...")

    try:
        # Use aiohttp for asynchronous requests
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        # Extract list of player names
        player_names = data.get("players", {}).get("list", [])

        if player_names:
            # Create the response message with player usernames
            result_message = "**👥 Players currently online:**\n" + "\n".join(player_names)
        else:
            result_message = "No players are currently online."

    except Exception as e:
        result_message = "An error occurred while fetching the players list."
        print(f"Error: {e}")  # Log error for debugging purposes

    # Edit the loading message with the players list or error message
    await loading_message.edit_text(result_message)

@app.on_message(filters.command("json"))
async def get_json_response(client, message):

    # Send a loading message
    loading_message = await message.reply("Fetching JSON response...")

    try:
        # Use aiohttp for asynchronous requests
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data. HTTP status code: {response.status}")

                data = await response.json()

        # Define the file path
        file_path = "minecraft_server_status.txt"

        # Write the JSON data to a text file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        # Send the text file to the user
        await client.send_document(message.chat.id, file_path, caption="Here is the JSON response.")

        # Clean up the file after sending
        os.remove(file_path)

    except Exception as e:
        result_message = "An error occurred while fetching the JSON response."
        print(f"Error: {e}")  # Log error for debugging purposes
        await loading_message.edit_text(result_message)


app.add_handler(Client.on_message(filters.command('ping'),ping_command())

# Start the Pyrogram client
if __name__ == "__main__":
    app.run()
