# imports
import discord
from discord.ext import commands
import requests
import json
from tabulate import tabulate
import base64
import os
import math
import asyncio



# bot settings
token = "BOT_TOKEN_HERE"
client = commands.Bot(command_prefix="/")
client.remove_command("help")


# bot events
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Minecraft | /help "))
    print('{0.user} bot is ready'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send("Cooldown!! please retry in **{}s**.".format(math.ceil(error.retry_after)))
        await asyncio.sleep(5)
        await msg.delete()
        await asyncio.sleep(6)
    else:
        print(error, on_command_error)


# how many servers the bot in
@client.command(pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.user)
async def botservers(ctx):
    await ctx.send(str(len(client.guilds)) + " servers")

# bot ping
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx):
    async with ctx.typing():
        await ctx.send(f"**{round(client.latency *1000)}** milliseconds!")

# to logout the bot
@client.command(hidden=False, aliases=['Kill', 'logout', 'Logout'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def kill(ctx):
    async with ctx.typing():
        dev_id = 289106753277263872
        if dev_id == ctx.author.id:
            await ctx.send("The bot has logged out!")
            await client.logout()
            await client.close()
        else:
            await ctx.send("You don't have permission to this command.")


general = '''
    ``/uuid``  ``/namehistory``  ``/skin``  ``/cape`` 
    '''
servers = '''
    ``/server``  ``/hypixel``  ``/hivemc`` 
    '''
mods = '''  
    ``/ofcape``  ``/labycape`` 
    '''
links = '''
    [INVITE TO YOUR SERVER](https://discord.com/api/oauth2/authorize?client_id=752660836153163846&permissions=391232&scope=bot)
    '''

# help command
@client.command(pass_context=True, aliases=['Help'])
async def help(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            color = discord.Color.green()
        )

        embed.add_field(name="General", value=general, inline=False)
        embed.add_field(name="Servers", value=servers, inline=False)
        embed.add_field(name="Mods", value=mods, inline=False)
        embed.add_field(name="\u200b", value=f'{links}\n**Developer**: <@289106753277263872>', inline=False)
        await ctx.send(embed=embed)


####################################################################################################

# username to uuid 
def UUID(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        rsp = requests.get(url)
    except:
        print("Something went wrong!")
    try:
        data = rsp.json()
    except:
        return "Wrong username!"
    if rsp.status_code == 204 or rsp.status_code == 400:
        return "Wrong username!"
    elif rsp.text == '':
        return "Wrong username!"
    elif 'error' in rsp.text:
        return "Wrong username!"
    else:
        name = data['name']
        uid = data['id']
        return name, uid


# Minecraft uuid ####################################################################################

@client.command(aliases=['Uid', 'UID'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def uuid(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
    if not username:
        embed.add_field(name="Usage", value="``/uuid <username>``", inline=False)
        await ctx.send(embed=embed)

    uuid = UUID(username[0])[1] ; name = UUID(username[0])[0]

    if UUID(username[0]) == 'Wrong username!':
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/face/512/{uuid}")
        embed.add_field(name=f"{name}'s uuid", value=f"```{uuid}```", inline=False)
        await ctx.send(embed=embed)


# minecraft name history ##############################################################################

@client.command(aliases=['Namehistory', 'nh', 'NH'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def namehistory(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Usage", value="``/namehistory <username>``", inline=False)
            await ctx.send(embed=embed)

    url = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    try:
        rsp = requests.get(url=url)
    except:
        print("Something went wrong!")
    data = rsp.json()
    name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]

    if 'error' in rsp.text:
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        nhistory = data['username_history']
        nhistory = tabulate(nhistory,headers="keys")
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/head/512/{uuid}")
        embed.add_field(name=f"{name}'s name history", value=f"```{nhistory}```", inline=False)
        await ctx.send(embed=embed)


# minecraft skin ######################################################################################

@client.command(aliases=['Skin'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def skin(ctx, *args):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        username = None
        skin_part = "full"
        if len(args) == 1:
            username = args[0]
        elif len(args) == 2:
            username = args[0]
            skin_part = args[1]
        if not username:
            embed.add_field(name="Usage", value="``/skin <username>``\n ``/skin <username> <head>`` \nyou can choose between ``(face, head, bust, front, frontfull)`` for custom skin part.", inline=False)
            await ctx.send(embed=embed)

    uuid = UUID(username)[1] ; name = UUID(username)[0]

    if UUID(username[0]) == 'Wrong username!':
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        uuid = uuid

    url = f"https://visage.surgeplay.com/{skin_part}/512/{uuid}"
    try:
        rsp = requests.get(url=url)
    except:
        print("Something went wrong!")

    if "400" in rsp.text:
        await ctx.send("**ERROR!!** Wrong skin part!")
    else:
        embed.set_image(url=url)
        embed.add_field(name=f"{name}'s Skin", value=f"\u200b", inline=False)
        await ctx.send(embed=embed)


# minecraft capes #####################################################################################

@client.command(aliases=['Cape'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def cape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Usage", value="``/cape <username>``", inline=False)
            await ctx.send(embed=embed)

    url = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    try:
        rsp = requests.get(url=url)
    except:
        print("Something went wrong!")
    data = rsp.json()
    name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]

    if 'error' in rsp.text:
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        if "cape" in data.get('textures'):
            cape = data['textures']['cape']['url']
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/frontfull/512/{uuid}")
            embed.add_field(name=f"{name}'s cape", value=f"\u200b", inline=False)
            embed.set_image(url=cape)
            await ctx.send(embed=embed)
        else:
            await ctx.send("**ERROR!!** You have no cape!")


# servers ###############################################################################

@client.command(aliases=['Server'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def server(ctx,*server):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        file = discord.File(r'D:\Omar\Python\Discord Bots\MinecraftBot\server_icon.png')
        if not server:
            embed.add_field(name="Usage", value="``/server <server_address>``", inline=False)
            await ctx.send(embed=embed)

    url = f"https://api.mcsrvstat.us/2/{server[0]}"
    try:
        rsp = requests.get(url=url)
    except:
        print("Something went wrong!")
    data = rsp.json()

    try:
        ip = data['ip']
        port = data['port']
        clean = data['motd']['clean']
        clean = ([c.strip() for c in clean])
        players1 = data['players']['online']
        players2 = data['players']['max']
        version = data['version']
        hostname = data['hostname']

        icon = data.get("icon").split(",")[1]
        with open("server_icon.png", "wb") as fh:
            fh.write(base64.decodebytes(icon.encode()))

        embed.set_thumbnail(url="attachment://server_icon.png")
        embed.add_field(name=f"{server[0]}'s status\n", value=f"```{clean[0]}\n{clean[1]}```**Hostname**: {hostname}\n**Players**: {players1}/{players2}\n**Version**: {version}\n**IP**: {ip}:{port}", inline=False)
        await ctx.send(file=file ,embed=embed)
    except:
        await ctx.send("**ERROR!!** Wrong server!")


# optifine capes ###############################################################################

@client.command(aliases=['Ofcape', 'of', 'OF'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def ofcape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.red()
        )
        if not username:
            embed.add_field(name="Usage", value="``/ofcape <username>``", inline=False)
            await ctx.send(embed=embed)

    name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]

    url = f"http://s.optifine.net/capes/{name}.png"
    try:
        rsp = requests.get(url)
    except:
        print("Something went wrong!")

    if "Not found" in rsp.text:
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/frontfull/512/{uuid}")
        embed.add_field(name=f"{name}'s optifine cape", value="\u200b", inline=False)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


# hypixel ######################################################################################

@client.command(aliases=['Hypixel'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def hypixel(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.red()
        )
        if not username:
            embed.add_field(name="Usage", value="``/hypixel <username>``", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
            await ctx.send(embed=embed)

    name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]

    url = "https://api.slothpixel.me/api/players/" + username[0]
    try:
        rsp = requests.get(url)
    except:
        print("Something went wrong!")
    data = rsp.json()

    if 'error' in rsp.text:
        await ctx.send("**ERROR!!** Wrong username!")
    else:
        rank = data['rank']
        level = int(data['level'])
        # clevel = ("%d" % level) # or clevel = ("{:d}".format(level))
        exp = data['exp']
        karma = data['karma']
        achievement_points = data['achievement_points']
        quests_completed = data['quests_completed']
        total_kills = data['total_kills']
        total_wins = data['total_wins']
        total_coins = data['total_coins']
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/512/{uuid}")
        embed.add_field(name=f"{name}'s stats", value=f"**Rank**: {rank}\n**Level**: {level}\n**Exp**: {exp}\n**Karma**: {karma}\n**Achievement points**: {achievement_points}\n**Quests completed**: {quests_completed}\n**Total kills**: {total_kills}\n**Total wins**: {total_wins}\n**Total coins**: {total_coins}", inline=False)
        await ctx.send(embed=embed)


# Hivemc #######################################################################################

@client.command(aliases=['Hivemc'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def hivemc(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.gold()
        )
        if not username:
            embed.add_field(name="Hivemc", value="**ERROR!!** Username not supplied!\nCommand example: ``/hivemc <username>``", inline=False)
            await ctx.send(embed=embed)

    name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]

    url = "https://api.hivemc.com/v1/player/" + username[0]
    try:
        rsp = requests.get(url=url)
    except:
        print("Something went wrong!")
    try:
        data = rsp.json()
    except:
        data = {}
    try:
        rank = data['modernRank']['human']
        medals = data['medals']
        tokens = data['tokens']
        medals = data['medals']
        creditss = data['credits']
        embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/512/{uuid}")
        embed.add_field(name=f"{name}'s stats", value=f"**Rank**: {rank}\n**Tokens**: {tokens}\n**Medals**: {medals}\n**Medals**: {medals}\n**Credits**: {creditss}", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("**ERROR!!** Wrong username or no data found!")


client.run(token)
