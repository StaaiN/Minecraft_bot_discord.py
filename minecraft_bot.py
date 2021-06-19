# imports
import discord
from discord.ext import commands
import requests
import json
from tabulate import tabulate
import base64
import math
import asyncio


# bot settings
token = "TOKEN_HERE"
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
        await ctx.send(f"**{round(client.latency *1000)}**ms")

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
    ``/ofcape``
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
        embed.add_field(name="Etc", value=f'``/ping``\n{links}\n**Developer**: <@289106753277263872>', inline=False)
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
        return False
    if rsp.status_code == 204 or rsp.status_code == 400:
        return "Wrong username!"
    elif rsp.text == '':
        return "Wrong username!"
    elif 'error' in rsp.text:
        return "Wrong username!"
    else:
        name = str(data['name'])
        uid = str(data['id'])
        return name, uid


# Minecraft uuid ####################################################################################

@client.command(aliases=['Uuid'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def uuid(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
    if not username:
        embed.add_field(name="Usage", value="``/uuid <username>``", inline=False)
        await ctx.send(embed=embed)
        return

    try:
        uuid = UUID(username[0])[1] ; name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    embed.set_thumbnail(url=f"https://cravatar.eu/helmavatar/{name}/190.png")
    embed.add_field(name=f"{name}'s uuid", value=f"```{uuid}```", inline=False)
    await ctx.send(embed=embed)


# minecraft name history ##############################################################################

@client.command(aliases=['Namehistory'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def namehistory(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Usage", value="``/namehistory <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    url = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    try:
        rsp = requests.get(url=url)
        data = rsp.json()
    except:
        await ctx.send("Something went wrong!")

    try:
        name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    nhistory = data['username_history']
    nhistory = tabulate(nhistory,headers="keys")
    embed.set_thumbnail(url=f"https://cravatar.eu/helmhead/{name}/190.png")
    embed.add_field(name=f"{name}'s name history", value=f"```{nhistory}```", inline=False)
    await ctx.send(embed=embed)


# minecraft skin ######################################################################################

@client.command(aliases=['Skin'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def skin(ctx, *username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Usage", value="``/skin <username>``", inline=False)
            await ctx.send(embed=embed)
            return
    try:
        name = UUID(username[0])[0] ; uuid = UUID(username[0])[1]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    url = f"https://minepic.org/skin/512/{name}"
    try:
        rsp = requests.get(url=url)
    except:
        await ctx.send("Something went wrong!")
        return

    if "400" in rsp.text:
        await ctx.send("**ERROR!!** Wrong skin part!")
    else:
        embed.set_image(url=url)
        embed.add_field(name=f"{name}'s skin", value=f"[Download](https://minepic.org/download/{uuid})", inline=False)
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
            return

    url = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    try:
        rsp = requests.get(url=url)
        data = rsp.json()
    except:
        await ctx.send("Something went wrong!")
        return

    try:
        name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    if "cape" in data.get('textures'):
        cape = data['textures']['cape']['url']
        embed.set_thumbnail(url=f"https://minotar.net/armor/bust/{name}/190.png")
        embed.add_field(name=f"{name}'s mojang cape", value=f"\u200b", inline=False)
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
        file = discord.File('./server_icon.png')
        if not server:
            embed.add_field(name="Usage", value="``/server <server_address>``", inline=False)
            await ctx.send(embed=embed)
            return

    url = f"https://api.mcsrvstat.us/2/{server[0]}"
    try:
        rsp = requests.get(url=url)
        data = rsp.json()
        status = data['online']
    except:
        await ctx.send("Something went wrong!")
        return

    if status == True:
        ip = data['ip']
        clean = data['motd']['clean']
        clean = "\n".join([a for a in clean])
        players1 = data['players']['online']
        players2 = data['players']['max']
        version = data['version']
        hostname = data['hostname']

        icon = data.get("icon").split(",")[1]
        with open("server_icon.png", "wb") as fh:
            fh.write(base64.decodebytes(icon.encode()))

        embed.set_thumbnail(url="attachment://server_icon.png")
        try:
            online_players = data['players']['list']
            online_players = "\n".join([a for a in online_players])
            embed.add_field(name=f"Server status", value=f"```{clean}```\n**Hostname**: {hostname}\n**IP**: {ip}\n**Version**: {version}\n**Online Players**: {players1}/{players2}\n``{online_players}``", inline=False)
        except:
            embed.add_field(name=f"Server status", value=f"```{clean}```\n**Hostname**: {hostname}\n**IP**: {ip}\n**Version**: {version}\n**Online Players**: {players1}/{players2}", inline=False)
        await ctx.send(file=file ,embed=embed)
    else:
        await ctx.send("**ERROR!!** Wrong server!")


# optifine capes ###############################################################################

@client.command(aliases=['Ofcape'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def ofcape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        color = discord.Color.red()
        )
        if not username:
            embed.add_field(name="Usage", value="``/ofcape <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    try:
        name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    url = f"http://s.optifine.net/capes/{name}.png"
    try:
        rsp = requests.get(url)
    except:
        await ctx.send("Something went wrong!")
        return

    if "Not found" in rsp.text:
        await ctx.send("**ERROR!!** No cape found!")
    else:
        embed.set_thumbnail(url=f"https://minotar.net/armor/bust/{name}/190.png")
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
            await ctx.send(embed=embed)
            return

    try:
        name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    url = "https://api.slothpixel.me/api/players/" + username[0]
    try:
        rsp = requests.get(url, timeout=5)
        data = rsp.json()
    except:
        await ctx.send("**ERROR!!** Something went wrong!")
        return

    rank = data['rank']
    level = int(data['level'])
    exp = data['exp']
    karma = data['karma']
    achievement_points = data['achievement_points']
    quests_completed = data['quests_completed']
    total_kills = data['total_kills']
    total_wins = data['total_wins']
    total_coins = data['total_coins']
    embed.set_thumbnail(url=f"https://minotar.net/armor/bust/{name}/190.png")
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
            embed.add_field(name="Usage", value="``/hivemc <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    try:
        name = UUID(username[0])[0]
    except:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    url = "https://api.hivemc.com/v1/player/" + username[0]
    try:
        rsp = requests.get(url=url)
        data = rsp.json()
    except:
        await ctx.send("Something went wrong!")
        return

    try:
        rank = data['modernRank']['human']
        medals = data['medals']
        tokens = data['tokens']
        medals = data['medals']
        creditss = data['credits']
        embed.set_thumbnail(url=f"https://minotar.net/armor/bust/{name}/190.png")
        embed.add_field(name=f"{name}'s stats", value=f"**Rank**: {rank}\n**Tokens**: {tokens}\n**Medals**: {medals}\n**Medals**: {medals}\n**Credits**: {creditss}", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("**ERROR!!** Wrong username or no data found!")


client.run(token)
