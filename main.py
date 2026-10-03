from flask import Flask
import threading
import discord
import os

# --- Ye Render ke port error ko fix karne ke liye hai ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    # Render 10000 port pe scan karta hai
    app.run(host='0.0.0.0', port=10000)

# Web server ko alag thread me chalao
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
    # Tera purana code yahi aayega
    pass

# Bot ko token se chalao
TOKEN = os.getenv("DISCORD_TOKEN")  # Render > Environment me daalna
if not TOKEN:
    print("[ERROR] DISCORD_TOKEN nahi mila! Environment Variable me daal")
else:
    client.run(TOKEN)
