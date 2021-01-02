
import html
import random, re
import requests as r

from telegram import Update, ParseMode, MAX_MESSAGE_LENGTH
from telegram.ext import Filters, CallbackContext, CommandHandler, run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown

from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.alternate import typing_action
from tg_bot import dispatcher, SUDO_USERS, SUPPORT_USERS
from tg_bot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler

import tg_bot.modules.helper_funcs.fun_strings as fun


@run_async
@typing_action
def truth(update, context):
    update.effective_message.reply_text(random.choice(fun.TRUTH))

@run_async
@typing_action
def dare(update, context):
    update.effective_message.reply_text(random.choice(fun.DARE))


#run
@run_async
@typing_action
def runs(update, context):
    update.effective_message.reply_text(random.choice(fun.RUN_STRINGS))



@run_async
@typing_action
def judge(update: Update, context: CallbackContext):
    judger = ["<b>is lying!</b>", "<b>is telling the truth!</b>"]
    rep = update.effective_message
    msg = ""
    msg = update.effective_message.reply_to_message
    if not msg:
        rep.reply_text("Reply to someone's message to judge them!")
    else:
        user = msg.from_user.first_name
    res = random.choice(judger)
    reply = msg.reply_text(f"{user} {res}", parse_mode=ParseMode.HTML)


@run_async
@typing_action
def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
def react(update: Update, context: CallbackContext):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text = reply_text(random.choice(REACTS))



@run_async
@typing_action
def slap(update, context):
    args = context.args
    msg = update.effective_message

    # reply to correct message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            msg.from_user.first_name, msg.from_user.id)
        

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                slapped_user.first_name, slapped_user.id
            )

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(context.bot.first_name, context.bot.id)
        user2 = curr_user

    temp = random.choice(fun.SLAP_TEMPLATES)
    item = random.choice(fun.ITEMS)
    hit = random.choice(fun.HIT)
    throw = random.choice(fun.THROW)

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


#sanitize a user - by @saitamarobot
@run_async
@typing_action
def sanitize(update: Update, context: CallbackContext):
    message = update.effective_message
    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    reply_animation = message.reply_to_message.reply_animation if message.reply_to_message else message.reply_animation
    reply_animation(
        random.choice(fun.GIFS), caption=f'*Sanitizes {name}*')


@run_async
@typing_action
def hug(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            msg.from_user.first_name, msg.from_user.id
        )

    user_id = extract_user(update.effective_message, args)
    if user_id:
        hugged_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if hugged_user.username:
            user2 = "@" + escape_markdown(hugged_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                hugged_user.first_name, hugged_user.id
            )

    # if no target found, bot targets the sender
    else:
        user1 = "Awwh! [{}](tg://user?id={})".format(
            context.bot.first_name, context.bot.id
        )
        user2 = curr_user

    temp = random.choice(fun.HUG_TEMPLATES)
    hug = random.choice(fun.HUG)

    repl = temp.format(user1=user1, user2=user2, hug=hug)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)



@run_async
@typing_action
def abuse(update, context):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.ABUSE_STRINGS))


@run_async
@typing_action
def dice(update, context):
    context.bot.sendDice(update.effective_chat.id)


@run_async
@typing_action
def shrug(update, context):
    # reply to correct message
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.SHGS))


@run_async
@typing_action
def decide(update, context):
    args = update.effective_message.text.split(None, 1)
    if len(args) >= 2:  # Don't reply if no args
        reply_text = (
            update.effective_message.reply_to_message.reply_text
            if update.effective_message.reply_to_message
            else update.effective_message.reply_text
        )
        reply_text(random.choice(fun.DECIDE))


@run_async
def yesnowtf(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    res = r.get("https://yesno.wtf/api")
    if res.status_code != 200:
        return msg.reply_text(random.choice(fun.DECIDE))
    else:
        res = res.json()
    try:
        context.bot.send_animation(
            chat.id, animation=res["image"], caption=str(res["answer"]).upper()
        )
    except BadRequest:
        return


@run_async
@typing_action
def table(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.TABLE))


@run_async
@typing_action
def cri(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.CRI))


@run_async
@typing_action
def recite(update, context):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun.BEING_LOGICAL))


@run_async
def gbun(update, context):
    user = update.effective_user
    chat = update.effective_chat

    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in SUDO_USERS or int(user.id) in SUPPORT_USERS:
        context.bot.sendMessage(chat.id, (random.choice(fun.GBUN)))


@run_async
def gbam(update, context):
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    message = update.effective_message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        gbam_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(gbam_user.first_name)

    else:
        user1 = curr_user
        user2 = bot.first_name


    if update.effective_message.chat.type == "private":
        return
    if int(user.id) in SUDO_USERS or int(user.id) in SUPPORT_USERS:
        gbamm = fun.GBAM
        reason = random.choice(fun.GBAM_REASON)
        gbam = gbamm.format(user1=user1, user2=user2, chatid=chat.id, reason=reason)
        context.bot.sendMessage(chat.id, gbam, parse_mode=ParseMode.HTML)



@run_async
@typing_action
def shout(update, context):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif args:
        data = " ".join(args)
    else:
        data = ("I need a message to meme")

    msg = "```"
    result = []
    result.append(' '.join(list(data)))
    for pos, symbol in enumerate(data[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = data[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")

REACTS = (
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
)

@run_async
@typing_action
def copypasta(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to make pasta.")
    else:
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰",
        ]
        reply_text = random.choice(emojis)
        b_char = random.choice(
            message.reply_to_message.text
        ).lower()  # choose a random character in the message to be substituted with 🅱️
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        message.reply_to_message.reply_text(reply_text)


@run_async
@typing_action
def clapmoji(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to clap!")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        message.reply_to_message.reply_text(reply_text)


@run_async
@typing_action
def owo(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to meme.")
    else:
        faces = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            "\(^o\) (/o^)/",
            "( ^ _ ^)∠☆",
            "(ô_ô)",
            "~:o",
            ";____;",
            "(*^*)",
            "(>_",
            "(♥_♥)",
            "*(^O^)*",
            "((+_+))",
        ]
        reply_text = re.sub(r"[rl]", "w", message.reply_to_message.text)
        reply_text = re.sub(r"[ｒｌ]", "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r"[RL]", "W", reply_text)
        reply_text = re.sub(r"[ＲＬ]", "Ｗ", reply_text)
        reply_text = re.sub(r"n([aeiouａｅｉｏｕ])", r"ny\1", reply_text)
        reply_text = re.sub(r"ｎ([ａｅｉｏｕ])", r"ｎｙ\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"Ｎ([ａｅｉｏｕＡＥＩＯＵ])", r"Ｎｙ\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(faces), reply_text)
        reply_text = re.sub(r"！+", " " + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += " " + random.choice(faces)
        message.reply_to_message.reply_text(reply_text)


@run_async
@typing_action
def stretch(update, context):
    message = update.effective_message
    if not message.reply_to_message:
        message.reply_text("I need a message to streeeeeeeeetch.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])", (r"\1" * count), message.reply_to_message.text
        )
        if len(reply_text) >= MAX_MESSAGE_LENGTH:
            return message.reply_text(
                "Result of this message was too long for telegram!"
            )

        message.reply_to_message.reply_text(reply_text)


@run_async
@typing_action
def goodnight(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"Good Night! {escape_markdown(first_name)}" 
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


@run_async
@typing_action
def goodmorning(update, context):
    message = update.effective_message
    first_name = update.effective_user.first_name
    reply = f"Good Morning! {escape_markdown(first_name)}"
    message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


__help__ = """
*Some dank memes for fun or whatever!*
 - /hitler: Quote a message and type this command to make a caption of hitler.
 - /mock: Does the same as /hitler but spongemock instead.
 - /kim: Does the same as /hitler but with Kim Jong Un.
 - /trump: Does the same as /hitler but with  trump.
 - /sanitize: Sanitize Your Self.
 - /rmeme: Sends random meme scraped from reddit.
 - /meme: get some anime random meme
 - /shrug or /cri: Get shrug or ToT.
 - /decide: Randomly answer yes no etc.
 - /abuse: Abuses the retard!
 - /table: Flips a table...
 - /runs: Reply a random string from an array of replies.
 - /slap: Slap a user, or get slapped if not a reply.
 - /pasta: Famous copypasta meme, try and see.
 - /clap: Claps on someones message!
 - /owo: UwU-fy whole text XD.
 - /roll: Rolls a dice.
 - /recite: Logical quotes to change your life.
 - /stretch:  streeeeeeetch iiiiiiit.
 - /hug: Hug a user warmly, or get hugged if not a reply.
 - /pat: pats a user, or get patted
 - /shout: write anything you want to give loud shout
 - /truth or /dare: Send random truth or dare.
 - /judge : judge the people if they are saying truth.
 - /decide : can be also used with regex like: saber? <question>: randomly answer "Yes, No" etc.

Some other regex filters are:
goodmorning, good morning or goodnight, good night.

Saber will reply random strings accordingly when these words are used!
All regex filters can be disabled incase u don't want... like: /disable goodnight.

""" 

__mod_name__ = "Memes"

PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)
TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
JUDGE_HANDLER = DisableAbleCommandHandler("judge", judge)
REACT_HANDLER = DisableAbleCommandHandler("react", react)
SANITIZE_HANDLER = DisableAbleCommandHandler("sanitize", sanitize)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
DECIDE_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)^saber\?"), decide, friendly="decide"
)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse,pass_args=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs ,pass_args=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
GBUN_HANDLER = CommandHandler("gbun", gbun)
GBAM_HANDLER = CommandHandler("gbam", gbam)
TABLE_HANDLER = DisableAbleCommandHandler("table", table)
CRI_HANDLER = DisableAbleCommandHandler("cri", cri)
PASTA_HANDLER = DisableAbleCommandHandler("pasta", copypasta)
CLAP_HANDLER = DisableAbleCommandHandler("clap", clapmoji)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo)
STRECH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
RECITE_HANDLER = DisableAbleCommandHandler("recite", recite)
DICE_HANDLER = DisableAbleCommandHandler("roll", dice)
YESNOWTF_HANDLER = DisableAbleCommandHandler("decide", yesnowtf)
GDMORNING_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(goodmorning|good morning)"), goodmorning, friendly="goodmorning"
)
GDNIGHT_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"(?i)(goodnight|good night)"), goodnight, friendly="goodnight"
)


dispatcher.add_handler(REACT_HANDLER)
dispatcher.add_handler(JUDGE_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(SANITIZE_HANDLER)
dispatcher.add_handler(GBAM_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(GBUN_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(RECITE_HANDLER)
dispatcher.add_handler(CRI_HANDLER)
dispatcher.add_handler(PASTA_HANDLER)
dispatcher.add_handler(CLAP_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRECH_HANDLER)
dispatcher.add_handler(DICE_HANDLER)
dispatcher.add_handler(YESNOWTF_HANDLER)
dispatcher.add_handler(GDMORNING_HANDLER)
dispatcher.add_handler(GDNIGHT_HANDLER)




