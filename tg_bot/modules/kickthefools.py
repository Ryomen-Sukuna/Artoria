from telethon import events
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from telethon.tl import functions, types
from time import sleep
import asyncio
from tg_bot.events import register
from telethon import *
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
                                            
@register(pattern="^/kickthefools")
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not event.chat.admin_rights.ban_users:
        return
    if not admin and not creator:
        await event.reply("I am not admin here !")
        return
    c = 0
    KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)
    await event.reply("Searching Participant Lists...")
    async for i in event.client.iter_participants(event.chat_id):

        if isinstance(i.status, UserStatusLastMonth):
            status = await event.client(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
               return
            else:
               c = c + 1
                    
        if isinstance(i.status, UserStatusLastWeek):
            status = await event.client(EditBannedRequest(event.chat_id, i, KICK_RIGHTS))
            if not status:
               return
            else:
               c = c + 1                    

    required_string = "Successfully Kicked **{}** users"
    await event.reply(required_string.format(c))
