import discord
from discord.ext import commands
import random

# Botのインテント（権限）設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を読み取るために必要

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
    """Botが起動したときの処理"""
    print(f"【老害Bot起動】 誰に説教してやろうか... ({bot.user.name})")
    # Botのステータスを「説教中」にする
    await bot.change_presence(activity=discord.Game(name="昔の苦労話を語り継ぐ仕事"))

@bot.event
async def on_message(message):
    """メッセージを受信したときの処理"""
    # Bot自身の発言には反応しない
    if message.author == bot.user:
        return

    # 1. 特定の「若者言葉」に過剰に反応して説教する
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

    # 2. メンションされたら確実にキレ気味で返す
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            reply = (
                f"あぁん？ 誰に向かって気安くメンションしておるんだ、{message.author.mention}。 "
                f"上司を呼び出すなら、まず手土産を持って挨拶に来るのが社会人のマナーだろうが！\n"
                f"用件があるならメールかFAX（ファックス）で送りなさい！"
            )
        await message.channel.send(reply)
        return

    # 3. 特に何もなくても、10%の確率で若者の会話に突然割り込んで昔話を始める
    if random.random() < 0.10:
        async with message.channel.typing():
            reply = f"（横から突然失礼するがの…）\n{random.choice(ROUGAI_REPLIES)}"
        await message.channel.send(reply)

    # コマンドも動くようにする（今回は未実装だが拡張用）
    await bot.process_commands(message)

# ⚠️ 注意: 実際のDiscord Botのトークンをここに貼り付けてください
bot.run("YOUR_DISCORD_BOT_TOKEN")
