import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
from tg_bot.events import register
import random

@register(pattern="^/plet (.*)")
async def sticklet(event):
    sticktext = event.pattern_match.group(1)
    if not sticktext:
    	get = await event.get_reply_message()
    	sticktext = get.text
    if not sticktext:
    	await event.reply("`I need text to make sticker !`")
    	return
    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)
    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    font = ImageFont.truetype("/root/haruka/haruka/DejaVuSansMono.ttf", size=fontsize)
    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype("./haruka/DejaVuSansMono.ttf", size=fontsize)
    width, height = draw.multiline_textsize(sticktext, font=font)
    gg = ["red", "blue", "green", "yellow", "orange", "violet", "indigo"]
    hh = random.choice(gg)
    range = f"{hh}"
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=range)
    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)
    await event.client.send_file(event.chat_id, image_stream)

