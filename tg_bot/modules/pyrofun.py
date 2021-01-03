import re
import html
import regex
import aiohttp
from datetime import datetime
from asyncio import sleep
import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from tg_bot.utils.ut import get_arg
from tg_bot import pbot, LOGGER
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message


DART_E_MOJI = "🎯"
FOOTBALL_E_MOJI="⚽"
E_MOJI="🎰"

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


def convert(speed):
    return round(int(speed) / 1048576, 2)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def speedtest_callback(_, __, query):
    if re.match("speedtest", query.data):
        return True


speedtest_create = filters.create(speedtest_callback)


@pbot.on_message(filters.command("song"))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("Processing...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Song not found.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")



@pbot.on_message(filters.command('basket'))
async def basket(c: Client, m: Message):
    await c.send_dice(m.chat.id, reply_to_message_id=m.message_id, emoji="🏀")

@pbot.on_message(filters.command('dice'))
async def dice(c: Client, m: Message):
    dicen = await c.send_dice(m.chat.id, reply_to_message_id=m.message_id)
    await dicen.reply_text(f"The dice stopped at the number {dicen.dice.value}", quote=True)

@pbot.on_message(
    filters.command("dart")
)
async def throw_dart(client, message):
    """ /dart an @AnimatedDart """
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=DART_E_MOJI,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )


@pbot.on_message(
    filters.command("football")
)
async def throw_football(client, message):
    """ /football an @Animatedfootball """
    rep_mesg_id = message.message_id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.message_id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=FOOTBALL_E_MOJI,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )


@pbot.on_message(filters.command("dinfo") & filters.private)
async def ids_private(c: Client, m: Message):
    await m.reply_text("<b>Info:</b>\n\n"
                       "<b>Name:</b> <code>{first_name} {last_name}</code>\n"
                       "<b>Username:</b> @{username}\n"
                       "<b>User ID:</b> <code>{user_id}</code>\n"
                       "<b>Language:</b> {lang}\n"
                       "<b>Chat type:</b> {chat_type}".format(
                           first_name=m.from_user.first_name,
                           last_name=m.from_user.last_name or "",
                           username=m.from_user.username,
                           user_id=m.from_user.id,
                           lang=m.from_user.language_code,
                           chat_type=m.chat.type
                       ),
                       parse_mode="HTML")


@pbot.on_message(filters.command("dinfo") & filters.group)
async def ids(c: Client, m: Message):
    data = m.reply_to_message or m
    await m.reply_text("<b>Info:</b>\n\n"
                       "<b>Name:</b> <code>{first_name} {last_name}</code>\n"
                       "<b>Username:</b> @{username}\n"
                       "<b>User ID:</b> <code>{user_id}</code>\n"
                       "<b>Datacenter:</b> {user_dc}\n"
                       "<b>Language:</b> {lang}\n\n"
                       "<b>Chat name:</b> <code>{chat_title}</code>\n"
                       "<b>Chat username:</b> @{chat_username}\n"
                       "<b>Chat ID:</b> <code>{chat_id}</code>\n"
                       "<b>Chat type:</b> {chat_type}".format(
                           first_name=html.escape(data.from_user.first_name),
                           last_name=html.escape(data.from_user.last_name or ""),
                           username=data.from_user.username,
                           user_id=data.from_user.id,
                           user_dc=data.from_user.dc_id,
                           lang=data.from_user.language_code or "-",
                           chat_title=m.chat.title,
                           chat_username=m.chat.username,
                           chat_id=m.chat.id,
                           chat_type=m.chat.type
                       ),
                       parse_mode="HTML")


@pbot.on_message(filters.regex(r'^s/(.+)?/(.+)?(/.+)?') & filters.reply)
async def sed(c: Client, m: Message):
    exp = regex.split(r'(?<![^\\]\\)/', m.text)
    pattern = exp[1]
    replace_with = exp[2].replace(r'\/', '/')
    flags = exp[3] if len(exp) > 3 else ''

    count = 1
    rflags = 0

    if 'g' in flags:
        count = 0
    if 'i' in flags and 's' in flags:
        rflags = regex.I | regex.S
    elif 'i' in flags:
        rflags = regex.I
    elif 's' in flags:
        rflags = regex.S

    text = m.reply_to_message.text or m.reply_to_message.caption

    if not text:
        return

    try:
        res = regex.sub(
            pattern,
            replace_with,
            text,
            count=count,
            flags=rflags,
            timeout=1)
    except TimeoutError:
        await m.reply_text("Oops, your regex pattern ran for too long.")
    except regex.error as e:
        await m.reply_text(str(e))
    else:
        await c.send_message(m.chat.id, f'<pre>{html.escape(res)}</pre>',
                             reply_to_message_id=m.reply_to_message.message_id)



class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@pbot.on_message(filters.command("spbinfo"))
async def lookup(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        if message.reply_to_message.forward_from:
            get_user = message.reply_to_message.forward_from.id
        else:
            get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_chat(get_user)
    except PeerIdInvalid:
        await message.reply_text("I don't know that User.")
        sleep(2)
        return
    url = f"https://api.intellivoid.net/spamprotection/v1/lookup?query={user.id}"
    a = await AioHttp().get_json(url)
    response = a["success"]
    if response == True:
        date = a["results"]["last_updated"]
        stats = f"**◢ Intellivoid• SpamProtection Info**:\n"
        stats += f' • **Updated on**: `{datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S %p")}`\n'
        stats += (
            f" • **Chat Info**: [Link](t.me/SpamProtectionBot/?start=00_{user.id})\n"
        )

        if a["results"]["attributes"]["is_potential_spammer"] == True:
            stats += f" • **User**: `USERxSPAM`\n"
        elif a["results"]["attributes"]["is_operator"] == True:
            stats += f" • **User**: `USERxOPERATOR`\n"
        elif a["results"]["attributes"]["is_agent"] == True:
            stats += f" • **User**: `USERxAGENT`\n"
        elif a["results"]["attributes"]["is_whitelisted"] == True:
            stats += f" • **User**: `USERxWHITELISTED`\n"

        stats += f' • **Type**: `{a["results"]["entity_type"]}`\n'
        stats += (
            f' • **Language**: `{a["results"]["language_prediction"]["language"]}`\n'
        )
        stats += f' • **Language Probability**: `{a["results"]["language_prediction"]["probability"]}`\n'
        stats += f"**Spam Prediction**:\n"
        stats += f' • **Ham Prediction**: `{a["results"]["spam_prediction"]["ham_prediction"]}`\n'
        stats += f' • **Spam Prediction**: `{a["results"]["spam_prediction"]["spam_prediction"]}`\n'
        stats += f'**Blacklisted**: `{a["results"]["attributes"]["is_blacklisted"]}`\n'
        if a["results"]["attributes"]["is_blacklisted"] == True:
            stats += (
                f' • **Reason**: `{a["results"]["attributes"]["blacklist_reason"]}`\n'
            )
            stats += f' • **Flag**: `{a["results"]["attributes"]["blacklist_flag"]}`\n'
        stats += f'**PTID**:\n`{a["results"]["private_telegram_id"]}`\n'
        await message.reply_text(stats, disable_web_page_preview=True)
    else:
        await message.reply_text("`cannot reach SpamProtection API`")
        await sleep(3)

@pbot.on_message(filters.command('casino'))
async def casino(c: Client, m: Message):
    await c.send_dice(m.chat.id, reply_to_message_id=m.message_id, emoji="🎰")
