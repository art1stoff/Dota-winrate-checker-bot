import discord
import requests

def get_hero_id(hero_name):
    try:
        response = requests.get("https://api.opendota.com/api/heroes")
        response.raise_for_status()
        heroes = response.json()

        for hero in heroes:
            if hero_name.lower() == hero['localized_name'].lower():
                return hero['id']
        return None

    except requests.exceptions.RequestException as e:
        return f"Error while requesting data: {e}"

def get_hero_winrate(hero_id):
    try:

        url = "https://api.opendota.com/api/heroStats"
        response = requests.get(url)
        response.raise_for_status()
        heroes_stats = response.json()

        for hero in heroes_stats:
            if hero['id'] == hero_id:
                winrate = hero['pro_win'] / hero['pro_pick'] * 100 if hero['pro_pick'] > 0 else 0
                return f"Winrate: {winrate:.2f}%"
        
        return "Statistics for hero not found."
    
    except requests.exceptions.RequestException as e:
        return f"Error while requesting data: {e}"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} started')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hero'):
        try:
            hero_name = ' '.join(message.content.split(' ')[1:])

            hero_id = get_hero_id(hero_name)
            if hero_id is None:
                await message.channel.send(f"Hero with name '{hero_name}' not found")
                return

            await message.channel.send(f"Hero's name: {hero_name}")

            hero_stats = get_hero_winrate(hero_id)
            await message.channel.send(hero_stats)
        except IndexError:
            await message.channel.send("Please enter the command in the format `!hero <hero name>`.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

client.run('TOKEN')
