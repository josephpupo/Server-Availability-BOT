# This example requires the 'message_content' intent.
from tcp_latency import measure_latency
from discord.ext import tasks, commands
import discord
import time

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(command_prefix = "!", intents=intents)
CHANNEL_ID = 1012610674146431047 #my server
#CHANNEL_ID = 525146458828308506 #my notes 
IP = "69.117.39.211"
PORT = 25565
prevState = []
pikachu = "https://media.wired.com/photos/5f87340d114b38fa1f8339f9/master/w_960,c_limit/Ideas_Surprised_Pikachu_HD.jpg"
allowed_mentions = discord.AllowedMentions(everyone = True)
cstatus=False; #current status of the server

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    myloop.start()

@client.event
async def on_message(message):
    online = discord.Embed(title = "SERVER STATUS", 
                          description = "the server is online :)", color=0x00FF00)
    offline = discord.Embed(title = "SERVER STATUS", 
                          description = "the server is offline :(", color=0xFF000)
    online.set_image(url = pikachu)
    offline.set_image(url = pikachu)

    if message.author == client.user:
        print(message.author)
        return

    if message.content.startswith("!status"):
        if(cstatus):
            await message.channel.send(content = message.author.mention, 
                                       embed = online, 
                                       allowed_mentions=allowed_mentions)
        else:
            await message.channel.send(content = message.author.mention,
                                        embed = offline,
                                        allowed_mentions = allowed_mentions)


@tasks.loop(seconds=10)
async def myloop():
    global prevState
    global cstatus
    channel = client.get_channel(CHANNEL_ID)
    lat = measure_latency(host = IP, port = PORT)


    #embed
    online = discord.Embed(title = "SERVER UPDATE", 
                          description = "the server is online :)", color=0x00FF00)
    
    offline = discord.Embed(title = "SERVER UPDATE", 
                          description = "the server is offline :(", color=0xFF000)
    online.set_image(url = pikachu)
    offline.set_image(url = pikachu)
    
    #print("lat: ", lat)
    #print("prevState: ", prevState)
    if(len(lat) != len(prevState)):
        prevState = lat
        #print('server is online')
        if(len(lat) != 0):
            cstatus = True;
            await channel.send(content = "@everyone the server is online!", embed = online, allowed_mentions=allowed_mentions)
        else:
            cstatus = False;
            await channel.send(content = "@everyone the server is now offline!", embed=offline, allowed_mentions=allowed_mentions)

client.run('MTA5Mzc0NDc5NzIzNzM3OTIzNQ.Gg7svU.22rxK37R7jYKNQtAxlPWHWpP-2ljMTvpJzyOe0')