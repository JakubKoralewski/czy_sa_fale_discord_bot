import discord
import logging
import os
import sys
import re
import random

# Set up logging.

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.warning('Program started.')

# Check if is on a remote location.

try:
    DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
    logging.debug('on_remote')
except:
    from config import DISCORD_TOKEN
    logging.debug('not on_remote')

# https://www.devdungeon.com/content/make-discord-bot-python

# Variables:
odpowiedzi = {
    'pyt_o_fale': [
        'Nie ma fal.'
    ]
}
basepath = os.path.dirname(__file__)
filepath = os.path.abspath(os.path.join(basepath, "..", "static", "tekst.txt"))
with open(filepath, 'r', encoding='UTF-8') as tekst:
    logging.info('otwieram plik z tekstem')
    tekst = tekst.read()
#print(tekst)

client = discord.Client()


def czy_pyta_o_fale(message: str) -> False or re.match:
    logging.info('funkcja czy_pyta_o_fale wywolana')
    logging.info(f'z argumentem {message}')
    # Czy zawiera '?'.
    znak_zapytania = re.compile(r'\?')
    znak_zapytania = re.search(znak_zapytania, message)
    if not znak_zapytania:
        logging.debug('nie zawiera znaku zapytania')
        return False
    # Czy pyta o fale.
    fale = re.compile(r'(fale)|(fal)', re.IGNORECASE)
    fale = re.search(fale, message)
    if not fale:
        logging.debug('nie zawiera fale, fal')
        return False
    return fale


def odpowiedz_pyt_o_fale() -> str:
    logging.info('wybieram losowo z odpowiedzi["py_o_fale"]')
    return str(random.choice(odpowiedzi['pyt_o_fale']))


@client.event
async def on_message(message: str):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    msg = None
    if message.content.startswith('!hello'):
        msg = 'Elo {0.author.mention}'.format(message)
    elif message.content.startswith('!tekst'):
        msg = tekst
    elif czy_pyta_o_fale(message.content):
        msg = odpowiedz_pyt_o_fale()

    await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    login_info = f'Logged in as {client.user.name}, id: {client.user.id}\n---------'
    logging.info(login_info)
    print(login_info)


client.run(DISCORD_TOKEN)
