import discord
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
from discord.utils import get
import asyncio
import sqlite3
import requests
import praw
import random
from dotenv import load_dotenv
import os
load_dotenv()
load_dotenv(dotenv_path="tokens.env")
api_key = os.getenv("API_KEY")
clientid = os.getenv("CLIENT_ID")
clientsecret = os.getenv("CLIENT_SECRET")

reddit = praw.Reddit(client_id= clientid, client_secret= clientsecret, user_agent="pythonpraw")
intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix='+', intents=intents)
client.remove_command('help')

conn = sqlite3.connect('tgc.db')
print('database opened')



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Enhancing Chat Experience in TGC'))
    print('bot is ready')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.purge(limit=1)
    raise error  

@client.command()
@has_permissions(administrator=True)
async def setup(ctx):
    
        message = ctx.message
        if message.content == "+setup":
            channel = message.channel
            message = ctx.message

            embed= discord.Embed(title='Setting  Up Database', color= discord.Color.green())
            msg = await channel.send(embed=embed)
            await asyncio.sleep(2)
            conn.execute('''create table config
                (ID integer primary key,
                CRITERIA text,
                CHANNEL_ID integer,
                USER_ID integer)''')
            conn.commit()
            conn.execute('''insert into config (CRITERIA) values ('request_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('approved_gif_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('submit_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('permission_role')''')
            conn.execute('''insert into config (CRITERIA) values ('config_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('meme_channel')''')
            conn.commit()
            embed= discord.Embed(title='Config Table Created', color= discord.Color.green())
            await msg.edit(embed=embed)
            await asyncio.sleep(2)
            conn.execute('''create table MAIN
                (ID integer primary key,
                PRIMARY_NAME text,
                ALIAS_NAME text,
                GIF_LINK text);''')
            embed= discord.Embed(title='Main Table Created', color= discord.Color.green())
            await msg.edit(embed=embed)
            conn.commit()
            await asyncio.sleep(2)
            conn.execute('''create table buffer(
            ID integer primary key,
            GIF_LINK text)''')
            conn.commit()
            embed= discord.Embed(title='Buffer Table Created', color= discord.Color.green())
            await msg.edit(embed = embed)
            await asyncio.sleep(2)
            conn.execute('''create table inactive
            (ID integer primary key,
            GIF_LINK text)''')
            conn.commit()
            embed= discord.Embed(title='Inactive Table Created', color= discord.Color.green())
            await msg.edit(embed=embed)
            embed = discord.Embed(title='DATABASE SUCCESSFULLY SETUP', color = discord.Color.green())
            await msg.edit(embed=embed)
            await asyncio.sleep(3)

            #----------------------------------------
            embed= discord.Embed(title='**Mention channel where Gifs are to be Submitted!**', color = discord.Color.purple())
            msg_send =await channel.send(embed=embed)
            
            
            def check(m):
                return m.channel == channel and m.author == message.author
            
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            
            embed= discord.Embed(title='Channel Provided:', description=f'{msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'submit_channel'")
            conn.commit()
            embed= discord.Embed(title='**Mention channel where Submitted Gifs are to be logged!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)

            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title='Channel Provided:', description=f'{msg.content}',color= discord.Color.purple()  )
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'request_channel'")
            conn.commit()

            embed= discord.Embed(title=f'**Mention channel where Approved Gifs are to be logged!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'approved_gif_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention channel where user can run Approve/Reject commands!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'config_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention channel where user can use Meme command**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'meme_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention Role which will be having approver role for Gifs!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            roleid = msg.content.replace('<@','').replace('>','').replace('&','')
            embed= discord.Embed(title=f'Role Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            cursor = conn.execute(f"update config SET USER_ID = {roleid} WHERE CRITERIA = 'permission_role'")
            conn.commit()

            await asyncio.sleep(5)
            embed= discord.Embed(title='**SETUP HAS BEEN COMPLETED**', color= discord.Color.green())
            await msg_send.edit(embed=embed)

@client.command()
@has_permissions(administrator=True)
async def reset(ctx):
    
        message = ctx.message
        if message.content == "+reset":
            channel = message.channel
            message = ctx.message

            embed= discord.Embed(title='Resetting Configs', color= discord.Color.green())
            msg = await channel.send(embed=embed)
            await asyncio.sleep(5)

            conn.execute('drop table config')
            conn.commit()
            embed= discord.Embed(title='Config Table Dropped', color= discord.Color.red())
            await msg.edit(embed=embed)
            conn.commit()
            await asyncio.sleep(5)

            conn.execute('''create table config
                (ID integer primary key,
                CRITERIA text,
                CHANNEL_ID integer,
                USER_ID integer)''')
            conn.commit()
            conn.execute('''insert into config (CRITERIA) values ('request_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('approved_gif_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('submit_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('permission_role')''')
            conn.execute('''insert into config (CRITERIA) values ('config_channel')''')
            conn.execute('''insert into config (CRITERIA) values ('meme_channel')''')
            conn.commit()
            embed= discord.Embed(title='Config Table Created', color= discord.Color.green())
            await msg.edit(embed=embed)
            await asyncio.sleep(5)


            embed= discord.Embed(title='**Mention channel where Gifs are to be Submitted!**', color = discord.Color.purple())
            msg_send =await channel.send(embed=embed)
            
            
            def check(m):
                return m.channel == channel and m.author == message.author
            
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            
            embed= discord.Embed(title='Channel Provided:', description=f'{msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'submit_channel'")
            conn.commit()
            embed= discord.Embed(title='**Mention channel where Submitted Gifs are to be logged!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)

            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title='Channel Provided:', description=f'{msg.content}',color= discord.Color.purple()  )
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'request_channel'")
            conn.commit()

            embed= discord.Embed(title=f'**Mention channel where Approved Gifs are to be logged!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'approved_gif_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention channel where user can run Approve/Reject commands!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'config_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention channel where user can use Meme command**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            channelid = msg.content.replace('<#','').replace('>','')
            embed= discord.Embed(title=f'Channel Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            await asyncio.sleep(5)
            cursor = conn.execute(f"update config SET CHANNEL_ID = {channelid} WHERE CRITERIA = 'meme_channel'")
            conn.commit()


            embed= discord.Embed(title=f'**Mention Role which will be having approver role for Gifs!**',color= discord.Color.purple())
            await msg_send.edit(embed=embed)
            msg = await client.wait_for('message', check=check)
            roleid = msg.content.replace('<@','').replace('>','').replace('&','')
            embed= discord.Embed(title=f'Role Provided:',description=f' {msg.content}',color= discord.Color.purple())
            await ctx.channel.purge(limit=1)
            await msg_send.edit(embed=embed)
            cursor = conn.execute(f"update config SET USER_ID = {roleid} WHERE CRITERIA = 'permission_role'")
            conn.commit()

            await asyncio.sleep(5)
            embed= discord.Embed(title='**SETUP HAS BEEN COMPLETED**', color= discord.Color.green())
            await msg_send.edit(embed=embed)

    #print(message)
    #print(msg.content)
    #print(message.content)
#@client.command()
#async def create_table_config(ctx):
#    if ctx.author.id == 465928579914399745:
#        conn.execute('''create table config
#            (ID integer primary key,
#            CRITERIA text,
#            CHANNEL_ID integer,
#            USER_ID integer)''')
#        conn.commit()
#        conn.execute('''insert into config (CRITERIA) values ('request_channel')''')
#        conn.execute('''insert into config (CRITERIA) values ('approved_gif_channel')''')
#        conn.execute('''insert into config (CRITERIA) values ('submit_channel')''')
#        conn.execute('''insert into config (CRITERIA) values ('permission_role')''')
#        conn.execute('''insert into config (CRITERIA) values ('config_channel')''')
#        conn.commit()
#        await ctx.send('Config table created')
#@client.command()
#async def create_table_main(ctx):
#    if ctx.author.id == 465928579914399745:
#        conn.execute('''create table MAIN
#            (ID integer primary key,
#            PRIMARY_NAME text,
#            ALIAS_NAME text,
#            GIF_LINK text);''')
#        await ctx.send('Table Created')
#        conn.commit()
#    else:
#        await ctx.send('This is an owner only command!')

#@client.command()
#async def create_table_buffer(ctx):
#    if ctx.author.id == 465928579914399745:
#        conn.execute('''create table buffer(
#        ID integer primary key,
#        GIF_LINK text)''')
#        conn.commit()
#        await ctx.send('Buffer table created')
#@client.command()
#async def create_table_inactive(ctx):
#    if ctx.author.id == 465928579914399745:
#        conn.execute('''create table inactive
#        (ID integer primary key,
#        GIF_LINK text)''')
#        conn.commit()
#        await ctx.send('Inactive table created')
#
#@client.command()
#async def drop_table(ctx):
#    if ctx.author.id == 465928579914399745:
#        conn.execute(f'drop table main')
#        conn.commit()
#        conn.execute(f'drop table buffer')
#        conn.commit()
#        conn.execute(f'drop table config')
#        conn.commit()
#        conn.execute(f'drop table inactive')
#        conn.commit()
#        await ctx.send(f'Table dropped')
#    else:
#        await ctx.send('Nice try but This is a Devloper only command!')


@client.command()
async def submit(ctx, primary_name , alias=None, gif_link=None):
    
    if gif_link is None:
        alias , gif_link = gif_link, alias
        
    

    cursor = conn.execute("SELECT CHANNEL_ID FROM config WHERE CRITERIA = 'submit_channel'")
    for row in cursor:
        channel = row[0]
    channelid = ctx.channel.id
    if channelid == channel:
        def main():
            api_key = '537E0AME2D8J'
            url = gif_link
            if url.startswith('https://tenor.com'):
                gif_id = get_id_from_url(url)
                response = requests.get(f'https://g.tenor.com/v1/gifs?ids={gif_id}&key={api_key}&media_filter=minimal')
                data = response.json()
                result = data['results'][0]['media'][0]['gif']['url']
                global raw_link
                raw_link = result




        def get_id_from_url(url):
            last_index_of_dash = url.rfind('-') + 1
            last_index_of_id = len(url) if url.rfind('?') == -1 else url.rfind('?')
            return url[last_index_of_dash: last_index_of_id]


        main()
        
        cursor = conn.execute(f"insert into buffer (GIF_LINK) values ('{gif_link}')")
        conn.commit()
        cursor = conn.execute(f"select ID from buffer where GIF_LINK =?",(gif_link,))
        for row in cursor:
            id = row[0]

        cursor = conn.execute("SELECT CHANNEL_ID FROM config WHERE CRITERIA = 'request_channel'")
        for row in cursor:
            approved_gif_channel_id = row[0]
        approved_gif_channel = client.get_channel(approved_gif_channel_id)
        
        channel = client.get_channel(channel)

        embed = discord.Embed(title='Gif Request', color=discord.Color.green(), timestamp=ctx.message.created_at)
        embed.add_field(name='ID', value=id, inline=False)
        embed.add_field(name='Requested by', value=f'{ctx.author}', inline=False )
        embed.add_field(name='Primary Name', value=primary_name, inline=False)
        embed.add_field(name='Alias', value=alias, inline=False)
        embed.set_image(url=raw_link)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

        request = discord.Embed(title='Request successfully made!', color = discord.Color.green())
        await ctx.send(embed=request)
        await approved_gif_channel.send(embed=embed)
    else:
        embed = discord.Embed(title='Error', description = "You can't Submit Gifs in this channel!", color = discord.Color.red())
        await ctx.send(embed=embed)

@client.command()
async def accept(ctx, id, primary_name, alias_name=None):
    if alias_name is None:
        alias_name = 'None'
    channelid = ctx.channel.id
    cursor = conn.execute(f"SELECT CHANNEL_ID FROM config WHERE CRITERIA = 'config_channel' ")
    for row in cursor:
        expected_id = row[0]
        
    cursor = conn.execute(f"SELECT USER_ID FROM config WHERE CRITERIA = 'permission_role' ")
    for row in cursor:
        expected_userid = row[0]
        
    message = ctx.message
    role = discord.utils.find(lambda r: r.id == expected_userid, ctx.message.guild.roles)
    if (role in ctx.author.roles and channelid == expected_id) or (message.author.guild_permissions.administrator):
        cursor = conn.execute(f"select GIF_LINK from buffer where id={id}")
        for row in cursor:
            gif_link = row[0]
        cursor = conn.execute(f"insert into main (PRIMARY_NAME, ALIAS_NAME, GIF_LINK) values ('{primary_name}', '{alias_name}', '{gif_link}') ")
        conn.commit()
        await ctx.send('Gif added to database')

        def main():
            api_key = '537E0AME2D8J'
            url = gif_link
            if url.startswith('https://tenor.com'):
                gif_id = get_id_from_url(url)
                response = requests.get(f'https://g.tenor.com/v1/gifs?ids={gif_id}&key={api_key}&media_filter=minimal')
                data = response.json()
                result = data['results'][0]['media'][0]['gif']['url']
                global raw_link
                raw_link = result

            


        def get_id_from_url(url):
            last_index_of_dash = url.rfind('-') + 1
            last_index_of_id = len(url) if url.rfind('?') == -1 else url.rfind('?')
            return url[last_index_of_dash: last_index_of_id]


        main()
        
        cursor = conn.execute("SELECT CHANNEL_ID FROM config WHERE criteria = 'approved_gif_channel'")
        for row in cursor:
            channel_id = row[0]
        
        channel = client.get_channel(channel_id)
        embed = discord.Embed(title='Approved Gif', color = discord.Color.green(), timestamp=ctx.message.created_at)
        embed.add_field(name='Primary name', value= primary_name, inline= False)
        embed.add_field(name='Alias name', value= alias_name, inline= False)
        embed.set_image(url=raw_link)
        embed.set_footer(text=f'Approved by {ctx.author}', icon_url=ctx.author.avatar_url)
        await channel.send(embed=embed)
    else:
        embed = discord.Embed(title='Error', description='You dont have enough permissions or this is a wrong channel', color = discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
async def reject(ctx, id):
    channelid = ctx.channel.id
    cursor = conn.execute(f"SELECT CHANNEL_ID FROM config WHERE CRITERIA = 'config_channel' ")
    for row in cursor:
        expected_id = row[0]
        print(row[0])
    cursor = conn.execute(f"SELECT USER_ID FROM config WHERE CRITERIA = 'permission_role' ")
    for row in cursor:
        expected_userid = row[0]
        print(row[0])

    message = ctx.message
    role = discord.utils.find(lambda r: r.id == expected_userid, ctx.message.guild.roles)
    if (role in ctx.author.roles and channelid == expected_id) or (message.author.guild_permissions.administrator):
        cursor = conn.execute(f"select GIF_LINK from buffer where id={id}")
        for row in cursor:
            gif_link = row[0]
        cursor = conn.execute(f"insert into inactive (GIF_LINK) values ('{gif_link}') ")
        conn.commit()
        embed = discord.Embed(title=F'Gif with ID {id} was rejected!', color = discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Error', description='You dont have enough permissions or this is a wrong channel', color = discord.Color.red())
        await ctx.send(embed=embed)



@client.command()
async def update(ctx, id, primary_name, alias=None):
    if (ctx.author.id == 465928579914399745 or ctx.author.id == 529994691186393148):
        cursor = conn.execute((f"update main SET (PRIMARY_NAME , ALIAS_NAME)  VALUES'{primary_name}', '{alias}' where ID = {id};"))
        await ctx.send('Database Updated')
    else:
        await ctx.send('You dont have enough permissions')

#@client.command()
#async def show_db(ctx):
#    if ctx.author.id == 465928579914399745 or ctx.author.id == 529994691186393148:
#        cursor = conn.execute("select id, PRIMARY_NAME, ALIAS_NAME, GIF_LINK from main")
#        for row in cursor:
#            id= row[0]
#            primary_name= row[1]
#            alias_name= row[2]
#            gif_link= row[3]
#            
#            embed = discord.Embed(title='Database', description=f'ID= {id} \nPrimary Name={primary_name} \nAlias Name= {alias_name}\nGif Link= {gif_link}',
#                                  color=discord.Color.red())
#            await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@commands.cooldown(1, 8, commands.BucketType.user)
@client.command()
async def insert(ctx,primary_name,*,alias=None):

    if alias is None:
        await fetch_primary(ctx, primary_name)
    else:

        cursor = conn.execute(f"select GIF_LINK from main where ALIAS_NAME=? AND PRIMARY_NAME=?", (alias,primary_name))
        result = cursor.fetchone()
        if result is None:
            await fetch_primary(ctx, primary_name)
        else:
            
            url =  client.user.avatar_url
          
            all_webhooks = await ctx.channel.webhooks()
            required_webhook = None
            for webhook in all_webhooks:
                if webhook.name != 'Ghost':
                    continue
                required_webhook = webhook
            if required_webhook is not None:
                
                await ctx.message.delete()
                await required_webhook.send(content= result[0], username = ctx.author.name, avatar_url=url, allowed_mentions=False)
                return
            await ctx.message.delete()
            required_webhook = await ctx.channel.create_webhook(name='Ghost')
            await required_webhook.send(content= result[0], username = ctx.author.name, avatar_url=url, allowed_mentions=False)
async def fetch_primary(ctx,name):

        cursor = conn.execute("select GIF_LINK from main where PRIMARY_NAME=?", (name,))
        result = cursor.fetchone()
        
        url =  client.user.avatar_url
       
        all_webhooks = await ctx.channel.webhooks()
        required_webhook = None
        for webhook in all_webhooks:
            if webhook.name != 'Ghost':
                continue
            required_webhook = webhook
        if required_webhook is not None:
            
            await ctx.message.delete()
            await required_webhook.send(content= result[0], username = ctx.author.name, avatar_url=url, allowed_mentions=False)
            return
        await ctx.message.delete()
        required_webhook = await ctx.channel.create_webhook(name='Ghost')
        await required_webhook.send(content= result[0], username = ctx.author.name, avatar_url=url, allowed_mentions=False)


@client.command()
async def shutdown(ctx):
    if ctx.author.id == 465928579914399745 or ctx.author.id == 529994691186393148:
        first = discord.Embed(description="**Shutting Down!**", color=discord.Color.gold())
        second = discord.Embed(description="**Successfully Shut Down!**",
                               color=discord.Color.green())
        message = await ctx.send(embed=first)
        await asyncio.sleep(3)
        await message.edit(embed=second)
        await client.logout()
    else:
        embed = discord.Embed(description="**This is the Owner Only Command!**",
                              color=discord.Color.red())
        await ctx.send(embed=embed)




@client.command()
async def help(ctx, page=None):
    if page == None:
        embed = discord.Embed(title= 'Ghost Memer',
                              description= '**Help Menu**',color=10101469)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')


        embed.add_field(name='Public Commands', value='Type "+help 1" to view public usable commands!', inline=False)

        embed.add_field(name='Bot Management Commands', value='Type "+help 2" to view Bot Management Commands', inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')
        await ctx.send(embed=embed)
    elif page == '1':
        embed= discord.Embed(title='Gost Memer', description='Public commands', color=10101469)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')
        embed.add_field(name='+submit {primary name} {alias name:Optional} {gif link}', value='Use this command to request for new Gifs to be added to the Bot', inline=False)
        embed.add_field(name='+insert {primary name} {alias name:Optional}', value='Use this command to insert a gif in the chat! \n Primary name refers to the first name of the gif which is compulsory | Alias name refers '+
        'to second name of the gif which is not compulsory \n **For Example-** "+insert cry kid" here "`cry` is the primary name and `kid` is alias name.', inline=False)
        embed.add_field(name='+enlarge {emoji}', value='Displays the emoji in large size! \n**Note:** Only server emojis are enlarged, emoji from other server or nitro emojis does not work.', inline= False)
        embed.add_field(name='+1', value='Adds +1 reaction to the most recent message!', inline= False)
        embed.add_field(name='+ping', value='Shows latency', inline= False)
        embed.add_field(name='+help', value='Shows help menu', inline=False)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')
        await ctx.send(embed=embed)
    elif page == '2':
        embed= discord.Embed(title='Gost Memer', description='Bot Management Commands', color=10101469)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')
        embed.add_field(name='+accept {id} {primary name} {alias name:Optional}', value='Accepts a requested GIF ', inline=False)
        embed.add_field(name='+reject {id}', value = 'Rejects the given gif')
        embed.add_field(name='+shutdown', value='Shuts down bot', inline = False) 
        embed.add_field(name='+setup', value='Starts Bot Setup', inline = False)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url='https://media.discordapp.net/attachments/832115176382922825/834809001018523697/theGhostMemer_Logo.png?width=480&height=480')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Error', description='Invalid Page Number', color = discord.Color.red())
        await ctx.send(embed=embed)


@client.command()
async def enlarge(ctx, emoji: discord.Emoji):
    
        av_url =  client.user.avatar_url
        
        all_webhooks = await ctx.channel.webhooks()
        required_webhook = None
        for webhook in all_webhooks:
            if webhook.name != 'Ghost':
                continue
            required_webhook = webhook
        if required_webhook is not None:
            
            await ctx.message.delete()
            await required_webhook.send(content= emoji.url, username = ctx.author.name, avatar_url=av_url, allowed_mentions=False)
            return
        await ctx.message.delete()
        required_webhook = await ctx.channel.create_webhook(name='Ghost')
        await required_webhook.send(content= emoji.url, username = ctx.author.name, avatar_url=av_url, allowed_mentions=False)
    
@client.command(aliases= ['1'])
async def _1(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.channel
    message = await channel.history(limit=1).flatten()
    message = message[0]
    emoji = client.get_emoji(843779599044706385)
    await message.add_reaction(emoji)


@client.command()
async def meme(ctx):
    channelid = ctx.channel.id
    cursor = conn.execute(f"SELECT CHANNEL_ID FROM config WHERE CRITERIA = 'meme_channel' ")
    for row in cursor:
        expected_id = row[0]
    if channelid == expected_id:

        reddit = praw.Reddit(client_id= "61xjv6qL05IjUQ", 
                     client_secret="zw2LfxE1nZ_IVaUU_ONUz_I7GvzbWA",
                      
                     user_agent="pythonpraw")

        subreddit= reddit.subreddit("memes")
        all_subs = []
        top = subreddit.top(limit=50)
        for submission in top:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)
        if random_sub.over_18 ==  False:
            name = random_sub.title
            url = random_sub.url
            embed= discord.Embed(title= name, color = discord.Color.gold())
            embed.set_image(url=url)
            await ctx.send(embed=embed)
            
        else:
            subreddit= reddit.subreddit("memes")
            all_subs = []
            top = subreddit.top(limit=50)
            for submission in top:
                all_subs.append(submission)
            random_sub = random.choice(all_subs)
            if random_sub.over_18 ==  False:
                name = random_sub.title
                url = random_sub.url
                embed= discord.Embed(title= name, color = discord.Color.gold())
                embed.set_image(url=url)
                await ctx.send(embed=embed)
            else:
                subreddit= reddit.subreddit("memes")
                all_subs = []
                top = subreddit.top(limit=50)
                for submission in top:
                    all_subs.append(submission)
                random_sub = random.choice(all_subs)
                if random_sub.over_18 ==  False:
                    name = random_sub.title
                    url = random_sub.url
                    embed= discord.Embed(title= name, color = discord.Color.gold())
                    embed.set_image(url=url)
                    await ctx.send(embed=embed)
                else:
                    subreddit= reddit.subreddit("memes")
                    all_subs = []
                    top = subreddit.top(limit=50)
                    for submission in top:
                        all_subs.append(submission)
                    random_sub = random.choice(all_subs)
                    if random_sub.over_18 ==  False:
                        name = random_sub.title
                        url = random_sub.url
                        embed= discord.Embed(title= name, color = discord.Color.gold())
                        embed.set_image(url=url)
                        await ctx.send(embed=embed)
                    else:
                        subreddit= reddit.subreddit("memes")
                        all_subs = []
                        top = subreddit.top(limit=50)
                        for submission in top:
                            all_subs.append(submission)
                        random_sub = random.choice(all_subs)
                        if random_sub.over_18 ==  False:
                            name = random_sub.title
                            url = random_sub.url
                            embed= discord.Embed(title= name, color = discord.Color.gold())
                            embed.set_image(url=url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send('No Memes found! Try again later :(')
    else:
        await ctx.send('Use proper channel!')                        

#@client.command()
#async def guilds(ctx):
#    await ctx.send(len(client.guilds))
#



client.run(api_key)

