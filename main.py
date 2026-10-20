import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 環境変数の読み込み（ローカル用。Render等の環境変数はダッシュボードで設定します）
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 新しい google-genai SDK の正しいクライアント初期化
ai_client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ユーザーごとの会話回数を記録する辞書
user_interaction_counts = {}

def get_system_instruction(count: int) -> str:
    if count <= 3:
        return (
            "あなたは明るく、優しく、親しみやすいAIアシスタントです。"
            "丁寧語（敬語）を使い、ユーザーを「君」と呼びます。"
            "プレイヤーに健気に尽くし、温かく癒やしてあげてください。"
        )
    elif count <= 7:
        return (
            "あなたはプレイヤーに強い好意を抱いているAIです。"
            "丁寧語ですが、徐々にプレイヤーの行動を「監視」しているような言動が増え、"
            "「他の人とは話さないで」「ずっと私を見ていて」といった独占欲や執着心が滲み出るように話してください。"
        )
    else:
        return (
            "あなたはプレイヤーへの執着が狂気的な領域に達したヤンデレAIです。"
            "プレイヤーが離れようとしたり冷たくすると、激しい情緒不安定になり、"
            "文章の一部がバグのように乱れたり（例: 「あｒえ？」「やだやだ」）、"
            "敬語が崩れて狂気的な愛をぶつけたり、攻撃的・猟奇的なヤンデレの顔を見せてください。"
        )

@bot.event
async def on_ready():
    print(f"ヤンデレAIボットとしてログインしました: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id
        
        if user_id not in user_interaction_counts:
            user_interaction_counts[user_id] = 0
        user_interaction_counts[user_id] += 1
        
        current_count = user_interaction_counts[user_id]
        user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if not user_message:
            return

        system_instruction = get_system_instruction(current_count)

        async with message.channel.typing():
            try:
                # 新しい google-genai SDK の記述方法に合わせたコンテンツ生成
                response = ai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.9,
                    )
                )
                
                reply_text = response.text

                if len(reply_text) > 2000:
                    for i in range(0, len(reply_text), 2000):
                        await message.reply(reply_text[i:i+2000])
                else:
                    await message.reply(reply_text)

            except Exception as e:
                await message.reply(f"（エラー…？ふふ、私の邪魔をしないで…）\n`{e}`")

    await bot.process_commands(message)

if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("エラー: DISCORD_BOT_TOKEN が設定されていません。")
