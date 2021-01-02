import json
import html
import bs4
import requests
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import (
    CallbackContext,
    run_async,
    CallbackQueryHandler)

info_btn = "More Information"
kaizoku_btn = "Kaizoku ☠️"
kayo_btn = "Kayo 🏴‍☠️"
ganime_btn = "Ganime ☠️"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"


def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)
    more_results = True

    try:
        search_query = args[1]
    except IndexError:
        message.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a['href']
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
           
    elif site == "ganime":
        search_url = f"https://gogoanime.so//search.html?keyword={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>gogoanime</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>gogoanime</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)
    else:
        message.reply_text(
            result, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@run_async
def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")


@run_async
def kayo(update: Update, context: CallbackContext):
    site_search(update, context, "kayo")
    
@run_async
def ganime(update: Update, context: CallbackContext):
    site_search(update, context, "ganime")
 
def anime_quote():
    url = "https://animechanapi.xyz/api/quotes/random"
    response = requests.get(url)
    # since text attribute returns dictionary like string
    dic = json.loads(response.text)
    quote = dic["data"][0]["quote"]
    character = dic["data"][0]["character"]
    anime = dic["data"][0]["anime"]
    return quote, character, anime


@run_async
def quotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change", callback_data="change_quote")]]
    )
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@run_async
def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change", callback_data="quote_change")]]
    )
    message.edit_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)



KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku)
KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo)
GANIME_SEARCH_HANDLER = DisableAbleCommandHandler("ganime", ganime)
QUOTE = DisableAbleCommandHandler("quote", quotes)
CHANGE_QUOTE = CallbackQueryHandler(change_quote, pattern=r"change_.*")
QUOTE_CHANGE = CallbackQueryHandler(change_quote, pattern=r"quote_.*")


dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(GANIME_SEARCH_HANDLER)
dispatcher.add_handler(QUOTE)
dispatcher.add_handler(CHANGE_QUOTE)
dispatcher.add_handler(QUOTE_CHANGE)

__handlers__ = [ KAIZOKU_SEARCH_HANDLER, KAYO_SEARCH_HANDLER,  GANIME_SEARCH_HANDLER]
