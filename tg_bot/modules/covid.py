import requests
from telegram import ParseMode, Update
from telegram.ext import run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def covid(update: Update, _):
    message = update.effective_message
    text = message.text.split(" ", 1)
    if len(text) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\n" \
                     f"Deaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\n" \
                     f"Active: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\n" \
                     f"Deaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\n" \
                     f"Deaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\n" \
                     f"Active: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\n" \
                     f"Deaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)
dispatcher.add_handler(COVID_HANDLER)
