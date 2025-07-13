import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import platform
import time

# === SETUP INTENTS & BOT ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# === FLASK KEEP-ALIVE ===
app = Flask('')


@app.route('/')
def home():
    return '''
    <html>
      <head><title>Bot is Alive</title></head>
      <body>
        <h1>✅ Discord Bot Aktif!</h1>
        <p>Ping by UptimeRobot atau cron-job berhasil.</p>
      </body>
    </html>
    '''


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# === KONFIGURASI ===
pesan_masuk = 0
PENGECUALIAN_AUTO = [1393560387814690917
                     ]  # Ganti dengan channel ID yang dikecualikan
start_time = time.time()


# === EVENT SAAT BOT AKTIF ===
@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai {bot.user.name}")
    await bot.change_presence(activity=discord.Game(name="Ketik !tolong"))


# === EVENT ON_MESSAGE + AUTO DELETE ===
@bot.event
async def on_message(message):
    global pesan_masuk

    if message.author.bot:
        return

    await bot.process_commands(message)

    if message.channel.id in PENGECUALIAN_AUTO:
        return

    pesan_masuk += 1
    if pesan_masuk >= 50:
        await message.channel.purge(limit=50)
        pesan_masuk = 0


# === COMMAND: !bersih ===
@bot.command(name="bersih",
             help="Hapus pesan secara manual. Contoh: !bersih 30")
@commands.has_permissions(manage_messages=True)
async def bersih(ctx, jumlah: int = 100):
    deleted = await ctx.channel.purge(limit=jumlah)
    await ctx.send(f"{len(deleted)} pesan telah dihapus!", delete_after=3)


# === COMMAND: !tolong ===
@bot.command(name="tolong", help="Menampilkan semua perintah bot")
async def custom_help(ctx):
    help_text = """
📖 **Menu Bantuan Bot:**

🔁 Auto-delete setiap 50 pesan (kecuali channel tertentu)

🧼 `!bersih` — Menghapus semua pesan  
🧼 `!bersih [jumlah]` — Menghapus pesan manual  
🙋 `!tolong` — Menampilkan bantuan ini  
💬 `!statuschat` — Lihat jumlah pesan masuk  
🤖 `!statusbot` — Info tentang bot
"""
    await ctx.send(help_text)


# === COMMAND: !status ===
@bot.command(name="status", help="Menampilkan menu pilihan status")
async def status(ctx):
    pesan = """
📊 **Menu Status Bot**

🧮 `!statuschat` — Lihat jumlah pesan masuk (sebelum auto-delete)  
🤖 `!statusbot` — Info bot: nama, ID, uptime, dll
"""
    await ctx.send(pesan)


# === COMMAND: !statuschat ===
@bot.command(name="statuschat", help="Lihat jumlah pesan yang sudah masuk")
async def statuschat(ctx):
    await ctx.send(f"📨 Jumlah pesan saat ini: **{pesan_masuk}/50**")


# === COMMAND: !statusbot ===
@bot.command(name="statusbot", help="Lihat status bot saat ini")
async def statusbot(ctx):
    uptime = time.time() - start_time
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    info = f"""
🤖 **Status Bot**
━━━━━━━━━━━━━━━━
📛 Nama Bot: `{bot.user.name}`
🆔 ID: `{bot.user.id}`
⏱️ Uptime: `{uptime_str}`
💻 Python: `{platform.python_version()}`
📚 Library: `discord.py`
📌 Server: `{len(bot.guilds)}`
💬 Prefix: `!`
"""
    await ctx.send(info)


# === JALANKAN BOT ===
keep_alive()
bot.run(
    "MTM5MzcxODAzMTM3MjI1OTQyMA.GvNw8M.nIptDS0wOP1D62Coi2wCoS2uRSIWGG5IUiIgik"
)  # Ganti dengan token asli
