# < (c) 2021 @Godmrunal >
#thanks to @Lost_In_The_Darkk
#kang with credit

import logging
import os
from os import remove

import requests
from decouple import config
from telethon import Button, TelegramClient, events
from telethon.errors.rpcerrorlist import PhotoInvalidDimensionsError
from htmlwebshot import WebShot


shot = WebShot()

Bot_Token = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

bot = TelegramClient(None, api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e").start(
    bot_token=Bot_Token)


logging.info("Starting bot...")


@bot.on(events.NewMessage(incoming=True, pattern="^/start"))
async def start_(event):
    await event.reply(
        "Hi {}!\nI am a Html Webshot bot. \n\n**Usage:** Send Link directly to bot To get your webshot".format(
            (await bot.get_entity(event.sender_id)).first_name
        ),
        buttons=[
            [
                Button.url("Repo", url="https://github.com/msy1717/htmlWebshot"),
                Button.url(
                    "Developer", url="https://t.me/Godmrunal"
                ),
            ],
            [Button.url("Channel", url="https://t.me/Botz_Official")],
        ],
    )


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def web_ss_capture(event):
    if event.text and not event.text.startswith("/") and not event.document:
        url = event.text
        xurl = ""
        xx = await event.reply("Getting info...")
        try:
            requests.get(url)
            xurl = url
        except requests.ConnectionError:
            return await xx.edit("Invalid URL!")
        except requests.exceptions.MissingSchema:
            try:
                requests.get("https://" + url)
                xurl = "https://" + url
            except requests.ConnectionError:
                try:
                    requests.get("http://" + url)
                    xurl = "http://" + url
                except requests.ConnectionError:
                    return await xx.edit("Invalid URL!")
        await xx.edit("Generating a webshot...")
        try:
            web_ss_path = shot.create_pic(url=xurl)
            await xx.edit("Uploading a webshot of `{}`".format(xurl))
            await bot.send_file(
                event.chat_id,
                file=web_ss_path,
                caption="**WebShot generated.**\n\n~ @Botz_Official",
            )
            await xx.delete()
            remove(web_ss_path)
         except Exception as e:
            await xx.edit(
                f"**ERROR**: \n`{e}`\n**URL**: `{xurl}`\n\nKindly forward this message to @BotzOfficial_Support."
            )
    elif event.document and event.file.name.endswith(".html"):
        xx = await event.reply("Downloading file.... Please wait..")
        path = await bot.download_file(event.document)
        await xx.edit("Generating a screenshot...")
        shot.create_pic(html=path, output="webss_bh.jpg")
        try:
            await event.reply(
                "**ScreenShot generated.**\n\n~ @Botz_Official", file="webss_bh.jpg"
            )
            await xx.delete()
        except PhotoInvalidDimensionsError:
            await event.reply(
                "**ScreenShot generated.**\n\n~ @Botz_Official", file="webss_bh.jpg",
                force_document=True
            )
            await xx.delete()

        try:
            remove("webss_bh.jpg")
        except Exception as e:
            logging.warning(e)

logging.info("\n\nBot has started.\n(c) @Godmrunal")

bot.run_until_disconnected()
