import datetime
from random import randint
from gtts import gTTS
import os
import re
import urllib
from datetime import datetime
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import requests
from typing import List
from telegram import ParseMode, InputMediaPhoto, Update, TelegramError, ChatAction
from telegram.ext import CommandHandler, run_async, CallbackContext
from tg_bot import dispatcher, TIME_API_KEY, CASH_API_KEY, WALL_API
from tg_bot.modules.disable import DisableAbleCommandHandler

opener = urllib.request.build_opener()

@run_async
def app(update: Update, _):
    message = update.effective_message
    try:
        progress_message = update.effective_message.reply_text(
            "Searching.... ")
        app_name = message.text[len('/app '):]
        remove_space = app_name.split(' ')
        final_name = '+'.join(remove_space)
        page = requests.get(
            f"https://play.google.com/store/search?q={final_name}&c=apps")
        soup = BeautifulSoup(page.content, 'lxml', from_encoding='utf-8')
        results = soup.findAll("div", "ZmHEEd")
        app_name = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'WsMG1c nnK0zc').text
        app_dev = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'KoLSrc').text
        app_dev_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('a', 'mnKHRc')['href']
        app_rating = results[0].findNext('div', 'Vpfmgd').findNext(
            'div', 'pf5lIe').find('div')['aria-label']
        app_link = "https://play.google.com" + results[0].findNext(
            'div', 'Vpfmgd').findNext('div', 'vU6FJ p63iDd').a['href']
        app_icon = results[0].findNext(
            'div', 'Vpfmgd').findNext(
            'div', 'uzcko').img['data-src']
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<code>Developer :</code> <a href='" + app_dev_link + "'>"
        app_details += app_dev + "</a>"
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐️ ").replace(" out of ", "/").replace(
                " stars", "", 1).replace(" stars", "⭐️").replace("five", "5")
        app_details += "\n<code>Features :</code> <a href='" + \
            app_link + "'>View in Play Store</a>"
        message.reply_text(
            app_details,
            disable_web_page_preview=False,
            parse_mode='html')
    except IndexError:
        message.reply_text(
            "No result found in search. Please enter **Valid app name**")
    except Exception as err:
        message.reply_text(err)
    progress_message.delete()

@run_async
def convert(update: Update, _):
    args = update.effective_message.text.split(" ", 3)
    if len(args) > 1:

        orig_cur_amount = float(args[1])

        try:
            orig_cur = args[2].upper()
        except IndexError:
            update.effective_message.reply_text(
                "You forgot to mention the currency code.")
            return

        try:
            new_cur = args[3].upper()
        except IndexError:
            update.effective_message.reply_text(
                "You forgot to mention the currency code to convert into.")
            return

        request_url = (
            f"https://www.alphavantage.co/query"
            f"?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={orig_cur}"
            f"&to_currency={new_cur}"
            f"&apikey={CASH_API_KEY}")
        response = requests.get(request_url).json()
        try:
            current_rate = float(
                response['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        except KeyError:
            update.effective_message.reply_text("Currency Not Supported.")
            return
        new_cur_amount = round(orig_cur_amount * current_rate, 5)
        update.effective_message.reply_text(
            f"{orig_cur_amount} {orig_cur} = {new_cur_amount} {new_cur}")
    else:
        update.effective_message.reply_text(__help__)





@run_async
def covid(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(' ', 1)
    if len(text) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(
            f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


APP_HANDLER = DisableAbleCommandHandler("app", app)
COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)
CONVERTER_HANDLER = DisableAbleCommandHandler('cash', convert)

dispatcher.add_handler(APP_HANDLER)
dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(CONVERTER_HANDLER)

__command_list__ = [
    "cash",
    "covid",
    "corona",
    "app"]
__handlers__ = [
    CONVERTER_HANDLER,
    APP_HANDLER]
