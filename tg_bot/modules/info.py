import html
import requests

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events 

from telegram import Update, ParseMode
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext
from telegram.error import BadRequest

from tg_bot import (DEV_USERS, OWNER_ID, SUDO_USERS, SUPPORT_USERS,
                           WHITELIST_USERS, dispatcher, client)
from tg_bot.__main__ import USER_INFO, TOKEN
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.sql.afk_sql import is_afk, check_afk_status
from tg_bot.modules.sql.users_sql import get_user_num_chats
from tg_bot.modules.helper_funcs.extraction import extract_user, get_user
import tg_bot.modules.sql.userinfo_sql as sql
import tg_bot.modules.helper_funcs.cas_api as cas
from telegram.utils.helpers import escape_markdown, mention_html

OFFICERS = [OWNER_ID] + DEV_USERS + SUDO_USERS 


@run_async
def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args) 

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
            not args or
        (len(args) >= 1 and not args[0].startswith("@") and
         not args[0].isdigit() and
         not message.parse_entities([MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    del_msg = message.reply_text("searching info data of user....",parse_mode=ParseMode.HTML)
    
    text = (f"<b>• User Information :-</b>\n\n"
            f"∘ ID: <code>{user.id}</code>\n"
            f"∘ First Name: {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\n∘ Last Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n∘ Username: @{html.escape(user.username)}"


    isafk = is_afk(user.id)
    try:
        text += "\n\n∘ Currently AFK: "
        if user.id == bot.id:
             text += "<code>???</code>"
        else:
             text += str(isafk)
    except:
         pass

    try:
        if user.id == bot.id:
           num_chats = "???"
        else:
           num_chats = get_user_num_chats(user.id)
       
        text += f"\n∘ Mutual Chats: <code>{num_chats}</code> "
    except BadRequest:
        pass
    
    
    try:
        status = status = bot.get_chat_member(chat.id, user.id).status
        if status:
               if status in "left":
                   text += "\n∘ Chat Status: <em>Not Here!</em>"
               elif status == "member":
                   text += "\n∘ Chat Status: <em>Is Here!</em>"
               elif status in "administrator":
                   text += "\n∘ Chat Status: <em>Admin!</em>"
               elif status in "creator": 
                   text += "\n∘ Chat Status: <em>Creator!</em>"
    except BadRequest:
        pass
    
    
    
    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\n∘ Admin Title: <code>{custom_title}</code> \n"
    except BadRequest:
        pass
   
    if user.id ==1286562476:
        text += "\n🚶🏻‍♂️Uff,This person is sudo \n HE IS is the cutie!."

    if user.id == OWNER_ID:
        text += "\nThis person is my Owner\nI would never do anything against him!."
        
    elif user.id in DEV_USERS:
        text += "\nThis person is my dev\nI would never do anything against him!."
        
    elif user.id in SUDO_USERS:
        text += "\nThis person is one of my sudo users! " \
                    "Nearly as powerful as my owner🕊so watch it.."
        
    elif user.id in SUPPORT_USERS:
        text += "\nThis person is one of my support users! " \
                        " He can gban you off the map."
        
       
    elif user.id in WHITELIST_USERS:
        text += "\nThis person has been whitelisted! " \
                        "That means I'm not allowed to ban/kick them."
    
       
    elif user.id == bot.id:
        text+= "\n\nI've Seen Them In... Wow. Are They Stalking Me? They're In All The Same Places I Am... Oh. It's Me.\n"

    text +="\n"
    text += "\nCAS banned: "
    result = cas.banchecker(user.id)
    text += str(result)
    for mod in USER_INFO:
        if mod.__mod_name__ == "info":
            continue

    for mod in USER_INFO:
        if mod.__mod_name__ == "Users":
            continue

        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n" + mod_info
    try:
        profile = bot.get_user_profile_photos(user.id).photos[0][-1]
        _file = bot.get_file(profile["file_id"])
        _file.download(f"{user.id}.png")

        message.reply_document(
        document=open(f"{user.id}.png", "rb"),
        caption=(text),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True)

    except IndexError:
        message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    finally:
        del_msg.delete()

    


@client.on(events.NewMessage(pattern="^[!/]id(?: |$)(.*)"))
async def useridgetter(target):
    replied_user = await get_user(target)
    user_id = target.from_id
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    first_name = first_name.replace("\u2060", "") if first_name else ("☠️ Deleted Account") 
    username = "@{}".format(username) if username else ("{}".format(first_name))

    await target.reply("**Name:** {} \n**User ID:** `{}`\n**Chat ID: `{}`**".format(
        username, user_id, str(target.chat_id)))



@client.on(
    events.NewMessage(
        pattern='/ginfo ',
        from_users=(OFFICERS or [])))
async def group_info(event) -> None:
    chat = event.text.split(' ', 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins)
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there."
        )
        return
    msg = f"**ID**: `{entity.id}`"
    msg += f"\n**Title**: `{entity.title}`"
    msg += f"\n**Datacenter**: `{entity.photo.dc_id}`"
    msg += f"\n**Video PFP**: `{entity.photo.has_video}`"
    msg += f"\n**Supergroup**: `{entity.megagroup}`"
    msg += f"\n**Restricted**: `{entity.restricted}`"
    msg += f"\n**Scam**: `{entity.scam}`"
    msg += f"\n**Slowmode**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**Username**: {entity.username}"
    msg += "\n\n**Member Stats:**"
    msg += f"\n`Admins:` `{len(totallist)}`"
    msg += f"\n`Users`: `{totallist.total}`"
    msg += "\n\n**Admins List:**"
    for x in totallist:
        msg += f"\n• [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**Description**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)




INFO_HANDLER = DisableAbleCommandHandler("info", info)

dispatcher.add_handler(INFO_HANDLER)
