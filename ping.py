from pyrogram import Client, filters
import aiohttp
import time

@Client.on_message(filters.command("ping"))
async def ping_command(client, message):
    
    # Send a loading message
    loading_message = await message.reply("Pinging ...")

    start_time = time.time()  # Capture the start time for ping calculation

    try:
        # Asynchronous request to the API for server data
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()

        # Calculate ping time (speed)
        ping_time = round((time.time() - start_time) * 1000)  # in milliseconds

        # Check if server is online and display speed
        if data.get("online"):
            result_message = f" **Ping**: {ping_time} ms"
        else:
            result_message = "The server is offline."

    except Exception as e:
        result_message = f"something is wrong : {e}"
        print(f"Error: {e}")

    # Edit the loading message with the result
    await loading_message.edit_text(result_message)
  
