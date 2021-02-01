#imports
import discord
from discord.ext import commands
import requests
import json
from tabulate import tabulate
import base64
import os
import math
import asyncio



token = "[TOKEN]"

client = commands.Bot(command_prefix="/")

client.remove_command("help")



@client.event
async def on_ready():
    # await client.change_presence(activity=discord.Game(".help | " + str(len(client.guilds)) + " Servers."))
    await client.change_presence(activity=discord.Game("Minecraft | /help "))
    print("Ready")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
       msg = await ctx.send("**ERROR!!** This command is on cooldown, please retry in **{}s**.".format(math.ceil(error.retry_after)))
       await asyncio.sleep(3) 
       await msg.delete()
       await asyncio.sleep(4)
    else:
        print(error)

 
@client.command(pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.user)
async def botservers(ctx):
    await ctx.send("I'm in " + str(len(client.guilds)) + " servers")


Minecrafticon = "https://media.discordapp.net/attachments/693211390508400662/726384171252973578/stain.png"


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

#help command
@client.command(pass_context=True, aliases=['Help'])
async def help(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            # title = "Help!",
            discription = "discription",
            color = discord.Color.green()
        )

        # embed.set_footer(text=)

        # embed.set_image(url=Minecrafticon)

        embed.set_thumbnail(url=Minecrafticon)

        embed.set_author(name="Commands",
        icon_url=Minecrafticon)

        embed.add_field(name="General", value=general, inline=False)

        embed.add_field(name="Servers", value=servers, inline=False)

        embed.add_field(name="Mods", value=mods, inline=False)

        embed.add_field(name="Links", value=f'{links}\n \nDeveloper: <@289106753277263872>', inline=False)

        await ctx.send(embed=embed)



# Minecraft uuid ####################################################################################

@client.command(aliases=['Uuid', 'UUID'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def uuid(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.green()
        )
    if not username:
        embed.add_field(name="Minecraft UUID", value="**ERROR!!**  Username not supplied!\nCommand example: ``/uuid <username>``", inline=False)
        await ctx.send(embed=embed)
        return

    minecrafturl = f"https://api.ashcon.app/mojang/v2/user/{username[0]}"
    mcurl = requests.get(url=minecrafturl)
    data = mcurl.json()

    if "username" in data and data.get("username") != 'null':
        uuid = data['uuid']
        embed.set_thumbnail(url=Minecrafticon)
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Minecraft UUID", value="Player: "f"**{username[0]}**\n"f"```{uuid}```", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("**ERROR!!** Wrong username!")

# minecraft name history
@client.command(aliases=['Namehistory', 'nh', 'NH'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def namehistory(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Minecraft Name History", value="**ERROR!!** Username not supplied!\nCommand example: ``/namehistory <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    nurl = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    nr = requests.get(url=nurl)
    data = nr.json()

    if "username" in data and data.get("username") != 'null':
        nhistory = data['username_history']
        nhistory = tabulate(nhistory,headers="keys")
        embed.set_thumbnail(url=Minecrafticon)
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Minecraft Name History", value="Player: "f"**{username[0]}**\n"f"```{nhistory}```", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("**ERROR!!** Wrong username!")

# minecraft skin
@client.command(aliases=['Skin'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def skin(ctx, *args):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
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
            embed.add_field(name="Minecraft Skin", value="**ERROR!!** Username not supplied!\nCommand example: ``/skin <username>`` or ``/skin <username> <head>`` you can choose between ``(face, head, bust, front, frontfull)`` for custom skin part.", inline=False)
            await ctx.send(embed=embed)
            return

    uuidurl = f"https://api.ashcon.app/mojang/v2/user/{username}"
    uid = requests.get(url=uuidurl)
    data = uid.json()
    if "username" in data and data.get("username") != 'null':
        uuid = data['uuid']
        originalskin = data['textures']['skin']['url']
        # slim = data['textures']['slim']
        if data['textures']['slim']:
            skintype = 'Alex'
        else:
            skintype = 'Steve'
    else:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    surl = f"https://visage.surgeplay.com/{skin_part}/512/{uuid}"
    sr = requests.get(url=surl)
    if "400" in sr.text:
        await ctx.send("**ERROR!!** Wrong skin part!")
    else:
        embed.set_image(url=surl)
        embed.set_thumbnail(url=Minecrafticon)
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Minecraft Skin", value="Player: "f"**{username}**\nType: **{skintype}**\n[Link]({originalskin})", inline=False)
        await ctx.send(embed=embed)

# minecraft capes
@client.command(aliases=['Cape'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def cape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.green()
        )
        if not username:
            embed.add_field(name="Minecraft Cape", value="**ERROR!!** Username not supplied!\nCommand example: ``/cape <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    curl = "https://api.ashcon.app/mojang/v2/user/" + username[0]
    cr = requests.get(url=curl)
    data = cr.json()

    if "username" in data and data.get("username") != 'null':
         if "cape" in data.get('textures'):
            cape = data['textures']['cape']['url']
            embed.set_thumbnail(url=Minecrafticon)
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
            embed.add_field(name="Minecraft Cape", value="Player: "f"**{username[0]}**\n[Link]({cape})", inline=False)
            embed.set_image(url=cape)
            await ctx.send(embed=embed)
         else:
            await ctx.send("**ERROR!!** There is no cape!")
    else:
        await ctx.send("**ERROR!!** Wrong username!")

################################################################################################


# optifine capes ###############################################################################

@client.command(aliases=['Ofcape', 'of', 'OF'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def ofcape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.red()
        )
        if not username:
            embed.add_field(name="Optifine Cape", value="**ERROR!!** Username not supplied!\nCommand example: ``/ofcape <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    ofcapee = (f"http://s.optifine.net/capes/{username[0]}.png")
    embed.set_image(url=ofcapee)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/710552597886664774/757620869483725028/dt6nhzuB_400x400.jpg")
    embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
    embed.add_field(name="Optifine Cape", value="Player: "f"**{username[0]}**\n[Link]({ofcapee})", inline=False)
    ourl = f"http://s.optifine.net/capes/{username[0]}.png"
    of = requests.get(url=ourl)
    if "Not found" in of.text:
        await ctx.send("**ERROR!!** Wrong username or there no cape, also make sure to put the username correctly in capital letters!")
    else:
        await ctx.send(embed=embed)

################################################################################################


# Labymod cape #################################################################################

@client.command(aliases=['Labycape', 'labymodcape', 'lbc'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def labycape(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.blue()
        )
        if not username:
            embed.add_field(name="Labymod Cape", value="**ERROR!!** Username not supplied!\nCommand example: ``/labycape <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    uuidurl = f"https://api.ashcon.app/mojang/v2/user/{username[0]}"
    uid = requests.get(url=uuidurl)
    data = uid.json()
    if "username" in data and data.get("username") != 'null':
        uuid = data['uuid']
    else:
        await ctx.send("**ERROR!!** Wrong username!")
        return

    lburl = f"https://www.labymod.net/page/php/getCapeTexture.php?cape&uuid={uuid}"
    lb = requests.get(url=lburl)
    if "not found" in lb.text:
        await ctx.send("**ERROR!!** Wrong username or there no cape!")
    else:
        embed.set_image(url=lburl)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/710552597886664774/757621809070997504/C0c1z0mn_400x400.jpg")
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Labymod Cape", value=f"Player: **{username[0]}**\n[Link]({lburl})", inline=False)
        await ctx.send(embed=embed)

# hypixel ######################################################################################

@client.command(aliases=['Hypixel'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def hypixel(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.red()
        )
        if not username:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/710552597886664774/757624630725837017/mUnwMuh3_400x400.png")
            embed.add_field(name="Hypixel", value="Hypixel general info ``/hypixel <username>``", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
            await ctx.send(embed=embed)
            return

    hurl = "https://api.slothpixel.me/api/players/" + username[0]
    hr = requests.get(url=hurl)
    data = hr.json()

    if "username" in data and data.get("username") != 'null':
        rank = data['rank']
        level = data['level']
        clevel = ("%d" % level) # or clevel = ("{:d}".format(level))
        exp = data['exp']
        karma = data['karma']
        achievement_points = data['achievement_points']
        quests_completed = data['quests_completed']
        total_kills = data['total_kills']
        total_wins = data['total_wins']
        total_coins = data['total_coins']
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/710552597886664774/757624630725837017/mUnwMuh3_400x400.png")
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Hypixel Stats", value="Player: "f"**{username[0]}**\n"f"═════✽═════\nRank: **{rank}**\nLevel: **{clevel}**\nExp: **{exp}**\nKarma: **{karma}**\nAchievement points: **{achievement_points}**\nQuests completed: **{quests_completed}**\nTotal kills: **{total_kills}**\nTotal wins: **{total_wins}**\nTotal coins: **{total_coins}**", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("**ERROR!!** Wrong username!")

################################################################################################


# Hivemc #######################################################################################

@client.command(aliases=['Hivemc', 'hv'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def hivemc(ctx,*username):
    async with ctx.typing():
        embed = discord.Embed(
        discription = "discription",
        color = discord.Color.gold()
        )
        if not username:
            embed.add_field(name="Hivemc", value="**ERROR!!** Username not supplied!\nCommand example: ``/hivemc <username>``", inline=False)
            await ctx.send(embed=embed)
            return

    hvurl = "https://api.hivemc.com/v1/player/" + username[0]
    hv = requests.get(url=hvurl)
    try:
        data = hv.json()
    except:
        data = {}

    if "username" in data and data.get("username") != 'null':
        rank = data['modernRank']['human']
        medals = data['medals']
        tokens = data['tokens']
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/710552597886664774/757633447840710716/uEAaSNCJ.png")
        embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by: {ctx.author}")
        embed.add_field(name="Hivemc Stats", value=f"Player: **{username[0]}**\n═════✽═════\nRank: **{rank}**\nTokens: **{tokens}**\nMedals: **{medals}**", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("**ERROR!!** Wrong username!")




client.run(token)
