import os
import random
import discord
from discord.ext import commands

# 1. 開発環境（ローカル）でのテスト用に、もし .env ファイルがあれば読み込む
# （Render上ではこの処理は無視され、ダッシュボードの環境変数が優先されます）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Botのインテント（権限）設定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 老害AIの小言リスト
ROUGAI_REPLIES = [
    "ふん、いまどきの若いもんは何でもかんでもチャットで済ませおって。昔はなぁ、用事があったら直接固定電話にダイヤル回して『〇〇君いますか！』って親父さんを呼び出したもんだぞ！",
    "おいおい、そんな短い略語ばかり使いおって。日本語が乱れておる。だいたい『エモい』ってなんだ、エモいって。ちゃんと『風情がある』と言えんのか！",
    "何がタイパだ、コスパだ。苦労して汗を流して泥水をすすってこそ一人前になれるんだよ。今の奴らはすぐに『効率』とか言って楽をしようとするから根性が育たんのだ。",
    "ふん、インターネットなんてものはなぁ、昔はテレホーダイの時間（23時）まで待って、ピーガガガガ…とモデムを鳴らしながら繋いだもんだ。今の高速回線はありがたみが足りん！",
    "そんなことGoogle（グーグル）で調べる前に、自分で図書館に行って百年の歴史を調べんか！ ネットの情報なんて全部嘘っぱちだと思え！",
    "私が君たちの年齢の頃はなぁ、残業代も出ないのに3日徹夜して会社に泊まり込んでコードを書き殴ったもんだ。それに比べて今の若いもんは、定時になったらすぐ退勤しおってからに……。",
    "なんだその『絵文字』は！ 男なら黙って！(文字化け)か、せめて『（笑）』か『（爆）』を使いなさい！ 派手なマークで誤魔化すんじゃない！"
]

@bot.event
async def on_ready():
    print(f"【老害Bot起動】 誰に説教してやろうか... ({bot.user.name})")
    await bot.change_presence(activity=discord.Game(name="昔の苦労話を語り継ぐ仕事"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 若者言葉の検知
    youth_words = ["エモい", "ガチで", "タイパ", "詰んだ", "草", "りょ", "ワンチャン"]
    if any(word in message.content for word in youth_words):
        async with message.channel.typing():
            reply = (
                f"おい、{message.author.mention}！ "
                f"なんだその言葉遣いは！ まーたそうやって若者言葉を使いおって。\n"
                f"{random.choice(ROUGAI_REPLIES)}"
            )
        await message.channel.send(reply)
        return

    # メンションされた時の反応
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            reply = (
                f"あぁん？ 誰に向かって気安くメンションしておるんだ、{message.author.mention}。 "
                f"上司を呼び出すなら、まず手土産を持って挨拶に来るのが社会人のマナーだろうが！\n"
                f"用件があるならメールかFAX（ファックス）で送りなさい！"
            )
        await message.channel.send(reply)
        return

    # 10%の確率で割り込み
    if random.random() < 0.10:
        async with message.channel.typing():
            reply = f"（横から突然失礼するがの…）\n{random.choice(ROUGAI_REPLIES)}"
        await message.channel.send(reply)

    await bot.process_commands(message)

# 2. 環境変数からトークンを安全に取得する
# Renderの管理画面で「Key: DISCORD_TOKEN」として値を設定してください
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ エラー: 環境変数 'DISCORD_TOKEN' が見つかりません。Renderの設定を確認してください。")
else:
    bot.run(TOKEN)
