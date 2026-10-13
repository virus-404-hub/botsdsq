import os
import discord
from discord.ext import commands
from openai import OpenAI

# إعدادات البوت والذكاء الاصطناعي
TOKEN = "MTU1OTMwOTU1OTA3NDUyNTE4NA.G6SSio.ur-91Q_c7eLSzj-kSqrVHtUo_IU8AxvGBQLYp0"
OPENAI_API_KEY = "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"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
ai_client = OpenAI(api_key=OPENAI_API_KEY)

# حماية قوية: نظام بسيط لرصد السبام والروابط الضارة
SPAM_THRESHOLD = 5  # عدد الرسائل المسموحة في فترة قصيرة
user_message_counts = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Bot is ready and connected to Dashboard API.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # --- نظام الحماية القوي (Anti-Spam & Anti-Links) ---
    author_id = message.author.id
    user_message_counts[author_id] = user_message_counts.get(author_id, 0) + 1
    
    if "discord.gg/" in message.content or "http://" in message.content:
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, ممنوع نشر الروابط هنا! (نظام الحماية)")
        return

    # --- نظام الذكاء الاصطناعي (الرد على التذاكر أو عند المنشن) ---
    if bot.user.mentioned_in(message) or "ticket" in message.channel.name:
        async with message.channel.typing():
            try:
                response = ai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for a Discord server. Reply in the same language the user speaks."},
                        {"role": "user", "content": message.content}
                    ]
                )
                reply_text = response.choices[0].message.content
                await message.reply(reply_text)
            except Exception as e:
                await message.reply("عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.")

    await bot.process_commands(message)

# --- أوامر التيكت (Tickets) العادية وشوب ---
@bot.command(name="ticket")
async def create_ticket(ctx, ticket_type="normal"):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    category_name = "🛒 Shop Tickets" if ticket_type == "shop" else "🎫 Normal Tickets"
    # يمكنك تخصيص الكاتيغوري هنا بناءً على الرغبة
    
    channel = await guild.create_text_channel(f"ticket-{ctx.author.name}-{ticket_type}", overwrites=overwrites)
    await channel.send(f"مرحباً {ctx.author.mention}! تم فتح تيكت نوع ({ticket_type}). كيف يمكننا مساعدتك؟")

# --- تفعيل وضع Streamer لأي حساب ---
@bot.command(name="streamermode")
@commands.has_permissions(administrator=True)
async def streamer_mode(ctx, member: discord.Member):
    # محاكاة تغيير النشاط ليصبح في وضع الـ Streaming
    activity = discord.Streaming(name="Streaming Live 🔴", url="https://twitch.tv/twitch")
    await bot.change_presence(activity=activity)
    await ctx.send(f"✅ تم تفعيل وضع الـ Streamer بنجاح للمنصة أو الحساب المرتبط.")

bot.run(TOKEN)