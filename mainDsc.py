import discord
import time
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import filters
from h import dscToken
from dotenv import load_dotenv

chatbot = ChatBot("Adrian Krawczyk",
                  filters = [filters.get_recent_repeated_responses],
                  logic_adapters = [
                      'chatterbot.logic.BestMatch',
                      'chatterbot.logic.MathematicalEvaluation'
                  ]
                  )

trainer = ListTrainer(chatbot)

conversation = [
    "Hej",
    "Dzień dobry",
    "Co tam słodziaku?",
    "zajebiscie",
    "ooo",
    "dzieki",
    "spoko kotku"
]

trainer.train(conversation)

client = discord.Client()
bot = commands.Bot(command_prefix='!')

# class CustomClient(discord.Client):
#     async def on_ready(self):
#         for guild in client.guilds:
#             if guild.name == GUILD:
#                 break
#
#         print(
#             f'{self.user} is connected to the following guild:\n'
#             f'{guild.name}(id: {guild.id})'
#         )
#
#     async def on_member_join(member):
#         await member.create_dm()
#         await member.dm_channel.send(
#             f'Hi {member.name}, welcome to my Discord server!'
#         )

@client.event
async def on_ready():
    for guild in client.guilds:
        # if guild.name == GUILD:
        #     break

        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    time.sleep(1)
    await message.channel.send(chatbot.get_response(message.content))

    time.sleep(1)
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

@bot.command()
async def baza(ctx):
    msg = ''
    for x in range(0, 100):
        msg += '['
        msg += str(chatbot.storage.get_random())
        msg += ']'
        msg += '\n'

    await ctx.send(msg)

@bot.command()
async def ping(ctx):
    await ctx.send(round(client.latency * 1000) + " ms")

# @client.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise
#

client.run(dscToken)
