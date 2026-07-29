# import os
# from dotenv import load_dotenv
# from langchain.messages import HumanMessage
# from agent import agent

# load_dotenv()

# import discord

# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     async with message.channel.typing():
#         content = message.content

#         response = await agent.ainvoke(
#             {"messages": [HumanMessage(content=content)]}
#         )

#         agent_message = response["messages"][-1].content

#         if isinstance(agent_message, list):
#             agent_message = agent_message[0]["text"]

#     await message.channel.send(agent_message)
# client.run(token=os.getenv("DISCORD_API_KEY"))


import os
import discord
from dotenv import load_dotenv
load_dotenv()
from langchain.messages import HumanMessage
from agent import agent # Make sure your agent has the generate_image tool attached
import asyncio


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    async with message.channel.typing():
        content = message.content

        # Invoke the LangChain agent
        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=content)]},
            config={"configurable":{"message":message},"loop":asyncio.get_event_loop()}
        )

        agent_message = response["messages"][-1].content

        if isinstance(agent_message, list):
            agent_message = agent_message[0]["text"]

        # --- NEW: Image Handling Logic ---
        files_to_send = []
        target_filename = "generated_image.png"
        
        # Check if the agent mentioned the image file in its response
        if target_filename in agent_message:
            if os.path.exists(target_filename):
                # Prepare the file for Discord
                files_to_send.append(discord.File(target_filename))
                
                # Optional: Clean up the raw filename from the chat message
                agent_message = agent_message.replace(target_filename, "").strip()
                
                # Ensure we don't send an empty message if the agent only output the filename
                if not agent_message:
                    agent_message = "Here is the image you requested:"

        # Send the message (and the file, if one exists)
        await message.channel.send(content=agent_message, files=files_to_send)

client.run(token=os.getenv("DISCORD_API_KEY"))