from flask import Flask, jsonify
import threading
import discord
import os
import json

# --- Flask Part (Render ke liye) ---
app = Flask(__name__)

DATA_FILE = "tiers.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Function jo tier add karega
def add_tier(name, dc, mode, rank):
    with open(DATA_FILE, "r") as f:
        players = json.load(f)

    found = False
    for p in players:
        if p["name"].lower() == name.lower():
            p.update({"dc": dc, "mode": mode, "rank": rank})
            found = True
            break
    if not found:
        players.append({"name": name, "dc": dc, "mode": mode, "rank": rank})

    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=2)

@app.route('/')
def home():
    return "Bot is running 24/7!"

@app.route('/api/tiers')
def get_tiers():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

def run_web():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_web, daemon=True).start()

# --- Tera Discord Bot ka code yaha se start ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[INFO] Logged in as {client.user}")
    print(f"[INFO] Bot is ready and connected!")

# Yaha apna Whaler se copy wala logic daal dena
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # EXAMPLE: Agar tu chat me likhega!addtier Venom @venom Crystal HT2
    if message.content.startswith("!addtier"):
        try:
            parts = message.content.split()
            #!addtier Name Discord Mode Rank
            name = parts[1]
            dc = parts[2]
            mode = parts[3]
            rank = parts[4]
            add_tier(name, dc, mode, rank)
            await message.channel.send(f"✅ Added {name} as {rank} in {mode} | Website updated!")
        except:
            await message.channel.send("Format: `!addtier Name @Discord Mode Rank`\nEx: `!addtier Venom @venom Crystal HT2`")

    # Tera purana code yahi aayega
    #...

# Bot Token
client.run(os.getenv("DISCORD_TOKEN"))
