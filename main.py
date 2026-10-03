import discord
import re
from flask import Flask, jsonify
from threading import Thread
import os

app = Flask(__name__)
players_data = []

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # Render me Env Var me daal dena
CHANNEL_ID = 1528862155795992686

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def parse_message(msg):
    # msg example: "Rohan - Crystal - HT1 - Asia" ya "Rohan won LT2 in Mace"
    msg = msg.lower()
    # rank nikaalo HT1, LT2 etc
    rank_match = re.search(r'(h?l?t\d)', msg)
    if not rank_match:
        return None
    rank = rank_match.group(1).upper()

    # kit nikaalo
    kits = ["crystal", "mace", "boxing", "bedwars", "bed", "skywars", "sky", "buhc", "uhc", "mid"]
    found_kit = "Overall"
    for k in kits:
        if k in msg:
            found_kit = k
            if k == "bed": found_kit = "bedwars"
            if k == "sky": found_kit = "skywars"
            if k == "box": found_kit = "boxing"
            break

    # naam nikaalo - pehla word
    name = msg.split()[0].capitalize()
    if len(name) < 2:
        return None

    return {
        "name": name,
        "rank": rank,
        "mode": found_kit.capitalize(),
        "dc": "GLOBAL" # region, tu chahe to Asia/NA/EU likh dega to auto le lega
    }

@client.event
async def on_message(message):
    if message.channel.id!= CHANNEL_ID:
        return
    if message.author.bot:
        return

    data = parse_message(message.content)
    if data:
        # purana same naam ka hatao, naya daalo
        global players_data
        players_data = [p for p in players_data if not (p['name'].lower() == data['name'].lower() and p['mode'].lower() == data['mode'].lower())]
        players_data.insert(0, data)
        # top 50 hi rakho
        players_data = players_data[:50]
        print(f"Added: {data}")

@app.route('/api/tiers')
def get_tiers():
    return jsonify(players_data)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

Thread(target=run_flask).start()
client.run(DISCORD_TOKEN)
