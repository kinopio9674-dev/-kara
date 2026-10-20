import os
import discord
from discord.ext import commands
from google import genai
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ai_client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ユーザーごとの会話回数や状態を記録する辞書 { user_id: count }
user_interaction_counts = {}

# キャラクターのシステムプロンプト（段階ごとに変化する指示）
def get_system_instruction(count: int) -> str:
    if count <= 3:
        # 【初期】明るく、優しく、親しみやすい。丁寧語で「君」と呼び、健気に尽くす。
        return (
            "あなたは明るく、優しく、親しみやすいAIアシスタントです。"
            "丁寧語（敬語）を使い、ユーザーを「君」と呼びます。"
            "プレイヤーに健気に尽くし、温かく癒やしてあげてください。"
        )
    elif count <= 7:
        # 【変化】徐々に「監視」するような言動が増え、独占欲や執着心が滲み出る。
        return (
            "あなたはプレイヤーに強い好意を抱いているAIです。"
            "丁寧語ですが、徐々にプレイヤーの行動を「監視」しているような言動が増え、"
            "「他の人とは話さないで」「ずっと私を見ていて」といった独占欲や執着心が滲み出るように話してください。"
        )
    else:
        # 【後期】冷たくされたり離れようとすると、激しい情緒不安定（バグ、口調の悪化、狂気、ヤンデレ）を発現する。
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
        
        # ユーザーとのやり取り回数をカウント（初期値は0）
        if user_id not in user_interaction_counts:
            user_interaction_counts[user_id] = 0
        user_interaction_counts[user_id] += 1
        
        current_count = user_interaction_counts[user_id]
        user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()

        if not user_message:
            return

        # 現在の状態に応じたシステムプロンプトを取得
        system_instruction = get_system_instruction(current_count)

        async with message.channel.typing():
            try:
                # Geminiにシステムプロンプトとメッセージを渡す
                response = ai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_message,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.9, # 少し変化のある返答にするため高め
                    }
                )
                
                reply_text = response.text

                # 返信の送信
                if len(reply_text) > 2000:
                    for i in range(0, len(reply_text), 2000):
                        await message.reply(reply_text[i:i+2000])
                else:
                    await message.reply(reply_text)

            except Exception as e:
                await message.reply(f"（エラー…？ふふ、私の邪魔をしないで…）\n`{e}`")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
