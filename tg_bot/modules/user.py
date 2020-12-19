"""Get Administrators of any Chat*
Syntax: .userlist"""
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors.rpcerrorlist import (UserIdInvalidError, MessageTooLongError, ChatAdminRequiredError)
                                                                                    
@register(pattern="^/users$")
async def get_users(show):
        if not show.is_group:
            await show.reply("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "Users in {}: \n".format(title)
        async for user in show.client.iter_participants(show.chat_id):
                  if not user.deleted:
                     mentions += f"\n[{user.first_name}](tg://user?id={user.id}) {user.id}"
                  else:
                      mentions += f"\nDeleted Account `{user.id}`"
        os.system('touch userslist.txt')
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
                show.chat_id,
                "userslist.txt",
                caption='Users in {}'.format(title),
                reply_to=show.id,
                )
        os.remove("userslist.txt")
