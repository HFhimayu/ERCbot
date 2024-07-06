import discord
import os
import datetime
import time
from discord.ext import tasks
from server import server_thread
import dotenv

dotenv.load_dotenv()

TOKEN = os.environ.get('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# bot started logs
@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  ch_name = 'bot-commands'
  for channel in client.get_all_channels():
    if channel.name == ch_name:
      await channel.send('deployed successfully or bot restarted!')

# Main
@client.event
async def on_message(message):

  # setup guild
  guild = message.guild  

  # return if sended from bot
  if message.author == client.user:
    return
  
  # user IDs
  author_1 = 647361970764251156 # admin
  author_2 = 1136700221603192873 # PaceManBot

  # return if sended from not admin and PaceManBot
  if message.author.id != author_1 and message.author.id != author_2:
    return

  # underscore fix
  fix_message = message.content.replace('ˍ', '_').replace(':enderpearl:', '<:enderpearl:1249680457050755092>').replace(':obsidian:', '<:obsidian:1249674953050030140>').replace(':blazerod:', '<:brazerod:1249674954623029258>')

  # get now time
  dt_now = datetime.datetime.now()

  # get Name from PaceMan
  n = fix_message.find('[')
  if n == -1:
    n = fix_message.find('Offline')

  # get PB Paces
  channel = discord.utils.get(message.guild.channels, name='pacemanbot-runner-pbpaces')
  pbpaces = await channel.fetch_message(channel.last_message_id) # msg ID
  split = pbpaces.content.replace('\n', '/').replace(' : ', '/')
  list_pbpaces = split.split('/')
  print(f'list_pbpaces: {list_pbpaces}')

  for i in range(0, len(list_pbpaces), 7):
    if list_pbpaces[i] in fix_message:
      print(f'find Name, PB Paces and PB: {list_pbpaces[i]}/{list_pbpaces[i+1]}/{list_pbpaces[i+2]}/{list_pbpaces[i+3]}/{list_pbpaces[i+4]}/{list_pbpaces[i+5]}/{list_pbpaces[i+6]}') # name/fs/ss/b/e/ee/pb
      # add :00
      for m in range(1, 6):
        if list_pbpaces[i+m].find(':') == -1:
          list_pbpaces[i+m] = f'{list_pbpaces[i+m]}:00'
      # rewrite pb if pb the None
      if list_pbpaces[i+6] == 'None':
        list_pbpaces[i+6] = '59:59'
      break


  # rewrite PaceMan message
  content = ''

  role = discord.utils.get(guild.roles, name="*FS30:0")
  if fix_message.find(f'{role.id}') != -1 and fix_message.find('Enter Bastion') != -1: # FS (Bastion)
    content = f'## <:bastion:1217191953830252584> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'

  if fix_message.find(f'{role.id}') != -1 and fix_message.find('Enter Fortress') != -1: # FS (Fortress)
    content = f'## <:fortress:1217191951972176053> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    # not exist a FSPB role

  role = discord.utils.get(guild.roles, name="*SS40:0")
  if fix_message.find(f'{role.id}') != -1 and fix_message.find('Enter Bastion') != -1: # SS (Bastion)
    content = f'## <:bastion:1217191953830252584> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+2]): # ss < pb pace
      role = discord.utils.get(guild.roles, name="*SSPB")
      content = f'## <:bastion:1217191953830252584> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]} <@&{role.id}>'

  if fix_message.find(f'{role.id}') != -1 and fix_message.find('Enter Fortress') != -1: # SS (Fortress)
    content = f'## <:fortress:1217191951972176053> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+2]): # ss < pb pace
      role = discord.utils.get(guild.roles, name="*SSPB")
      content = f'## <:fortress:1217191951972176053> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]} <@&{role.id}>'

  role = discord.utils.get(guild.roles, name="*B45:0")
  if fix_message.find(f'{role.id}') != -1: # B
    content = f'## <:portal:1217191949912637512> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+3]): # b < pb pace
      role = discord.utils.get(guild.roles, name="*BPB")
      content = f'## <:portal:1217191949912637512> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]} <@&{role.id}>'

  role = discord.utils.get(guild.roles, name="*E52:0")
  if fix_message.find(f'{role.id}') != -1: # E
    content = f'## <:sh:1217191958636658879> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+4]): # e < pb pace
      role = discord.utils.get(guild.roles, name="*EPB")
      content = f'## <:sh:1217191958636658879> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]} <@&{role.id}>'

  role = discord.utils.get(guild.roles, name="*EE55:0")
  if fix_message.find(f'{role.id}') != -1: # EE
    content = f'## <:end:1217191957017661530> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}**{fix_message[n-1:]}'
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+5]) and string_to_datetime(fix_message[3:fix_message.find(' -')]) - string_to_datetime('00:00') < string_to_datetime(list_pbpaces[i+6]) - string_to_datetime('00:48'): # ee < pb pace
      dif = string_to_datetime(list_pbpaces[i+6]) - string_to_datetime(fix_message[3:fix_message.find(' -')])
      role = discord.utils.get(guild.roles, name="*EEPB")
      content = f'## <:end:1217191957017661530> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}  (Exceed the PB in {convert_to_unix_time(dt_now, 0, 0, int(str(dif)[2:4]), int(str(dif)[5:]))})**{fix_message[n-1:]} <@&{role.id}>'

  if fix_message.find('Finish') != -1:
    role = discord.utils.get(guild.roles, name="NPB")
    if string_to_datetime(fix_message[3:fix_message.find(' -')]) < string_to_datetime(list_pbpaces[i+6]): # finish < pb
      dif = string_to_datetime(list_pbpaces[i+6]) - string_to_datetime(fix_message[3:fix_message.find(' -')])
      content = f'## <:credits:1217199823795519568>  New PB!!   {fix_message[2:n-1]}\r\n**FPB - {list_pbpaces[i+6]}  (-{str(dif)[2:]})**{fix_message[n-1:]}\n<@&{role.id}>'
    elif string_to_datetime(fix_message[3:fix_message.find(' -')]) == string_to_datetime(list_pbpaces[i+6]): # finish < pb
      dif = string_to_datetime(list_pbpaces[i+6]) - string_to_datetime(fix_message[3:fix_message.find(' -')])
      content = f'## <:credits:1217199823795519568>  New PB??   {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}  (±{str(dif)[2:]})**{fix_message[n-1:]}\n<@&{role.id}>'
    else: # finish > pb
      role = discord.utils.get(guild.roles, name="FIN")
      dif = string_to_datetime(fix_message[3:fix_message.find(' -')]) - string_to_datetime(list_pbpaces[i+6])
      content = f'## <:credits:1217199823795519568> {fix_message[2:n-1]}\r\n**PB - {list_pbpaces[i+6]}  (+{str(dif)[2:]})**{fix_message[n-1:]}\n<@&{role.id}>'


  # send Pace message
  # SSPB
  role = discord.utils.get(guild.roles, name="*SSPB") # SSPB role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # BPB
  role = discord.utils.get(guild.roles, name="*BPB") # BPB role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # EPB
  role = discord.utils.get(guild.roles, name="*EPB") # EPB role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # EEPB
  role = discord.utils.get(guild.roles, name="*EEPB") # EEPB role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # FIN (NPB)
  role = discord.utils.get(guild.roles, name="NPB") # NPB role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # FS
  role = discord.utils.get(guild.roles, name="*FS30:0") # FS role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # SS
  role = discord.utils.get(guild.roles, name="*SS40:0") # SS role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # B
  role = discord.utils.get(guild.roles, name="*B45:0") # B role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # E
  role = discord.utils.get(guild.roles, name="*E52:0") # E role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # EE
  role = discord.utils.get(guild.roles, name="*EE55:0") # EE role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return

  # FIN (FIN)
  role = discord.utils.get(guild.roles, name="FIN") # FIN role
  if f'@&{role.id}' in content:
    channel = discord.utils.get(message.guild.channels, name='not-pb-pace')
    await channel.send(content)
    print(f'sended message:\n{content}')
    return


  # working check
  if '!check' in fix_message:
    await message.channel.send('this bot is working!')
    return


# Defs
# https://stackoverflow.com/questions/72630298/adding-any-unix-timestamp-in-discord-py
def convert_to_unix_time(date: datetime.datetime, days: int, hours: int, minutes: int, seconds: int) -> str:
    # Get the end date
    end_date = date + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'


# https://gist.github.com/himoatm/e6a189d9c3e3c4398daea7b943a9a55d
def string_to_datetime(string):
    return datetime.datetime.strptime(string, '%M:%S')


# Server and TOKEN
server_thread()
client.run(TOKEN)