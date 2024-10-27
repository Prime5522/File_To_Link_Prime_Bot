import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote_plus
from helper_funcs import db, humanize
from config import AUTH_CHANNEL, URL, LOG_CHANNEL, SHORTLINK
from utils import get_name, get_hash, get_media_file_size, get_shortlink
import script

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton("✇ Jᴏɪɴ Oᴜʀ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ✇", url=chat.invite_link)])
        except Exception:
            pass
    return btn

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

    buttons = [
        [
            InlineKeyboardButton("✨ 𝗠𝗼𝘃𝗶𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 ⚡", url="https://t.me/Prime_Movies4U"),
            InlineKeyboardButton("💫 𝗔𝗱𝗺𝗶𝗻 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 💫", url="https://t.me/Prime_Bots_Support_RoBot")
        ],
        [InlineKeyboardButton("❤️‍🔥 𝗨𝗽𝗱𝗮𝘁𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🔥", url="https://t.me/Prime_botz")]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    m = await message.reply_sticker("CAACAgUAAxkBAAJ_9GcBHjuwkFd321YlOG4WOtdDCLv7AAIhFAACTiwJVPNa_9D21RH6NgQ")
    await asyncio.sleep(3)
    await m.delete()
    
    await client.send_photo(
        chat_id=message.from_user.id,
        photo="https://envs.sh/AH-.jpg",  # এখানে আপনার আগের ইমেজের লিঙ্ক দিন
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    btn = await is_subscribed(client, message, AUTH_CHANNEL)
    if btn:
        username = (await client.get_me()).username
        btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1] if len(message.command) > 1 else 'true'}")])
        await client.send_photo(
            chat_id=message.from_user.id,
            photo="https://envs.sh/AHX.jpg",
            caption=f"<b>👋 Hello {message.from_user.mention},\n\nIf you want to use me first you need to join our update channel.\n\nFirst, click on the \"✇ Join Our Updates Channel ✇\" button, then click on the \"Request to Join\" button.\n\nAfter that, click on the \"Try Again\" button.</b>",
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return

    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention 

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )
    fileName = quote_plus(get_name(log_msg))
    
    if SHORTLINK == False:
        stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}")
        download = await get_shortlink(f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}")
        
    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Fast Download 🚀", url=download), InlineKeyboardButton('🖥️ Watch online 🖥️', url=stream)]])
    )

    rm = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download)
            ]
        ] 
    )
    
    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ.\n\n ♨️ 𝗗𝗼𝗻'𝘁 𝗙𝗼𝗿𝗴𝗲𝘁 𝗧𝗼 𝗝𝗼𝗶𝗻: <a href=https://t.me/Prime_Botz>𝐏𝐑𝐈𝐌𝐄 𝐁𝐎𝐓z 🔥</a></b>"""

    await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(message)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
