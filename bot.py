import asyncio
import logging
import sys
from random import choice, random

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile, Message, ReplyParameters
from mcstatus import JavaServer

from config import JOKES, SERVER_IP, TOKEN

dp = Dispatcher()
server = JavaServer.lookup(SERVER_IP)


@dp.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer("НАТЯЖНЫЕ ПОТОЛКИ!!!")


@dp.message(Command("fabric"))
async def fabric_handler(msg: Message):
    if random() < 0.2:
        await msg.reply_animation(FSInputFile("dont_want.mp4"))
        return

    version = server.status().version.name

    if "paper" in version.lower():
        await msg.reply_sticker(
            "CAACAgIAAxkBAAEBhQ9onnKueTTsp7hr_E124X_B0_gUagACuVcAAsjL-Ui7nJ9NuU6u5DYE"
        )
        await msg.answer("Сегодня без фабрика")
    elif "fabric" in version.lower():
        await msg.reply_sticker(
            "CAACAgIAAxkBAAEBhRFonnK95LQOno1rIBAPz5nayMT6xQACaFEAAgZfAUm8ZNEHtoGQozYE"
        )
        await msg.answer("Урааааа фабрик")
    else:
        await msg.reply_sticker(
            "CAACAgIAAxkBAAEBhRNonnLnvKgcgSOBsZbB3hWlx29enQACt1oAAqo04UlB5uOhJfqPJzYE"
        )
        await msg.answer(f"шо це такое???? ({html.quote(version)})")


@dp.message(Command("players"))
async def players_handler(msg: Message):
    if random() < 0.2:
        await msg.reply_animation(FSInputFile("dont_want.mp4"))
        return

    status = server.status()

    ans = f"<b>Игроки</b> ({SERVER_IP}):\n • "

    if status.players.online == 0:
        ans += html.italic("Нет игроков онлайн!")
    else:
        ans += "\n • ".join(
            [html.quote(player.name) for player in status.players.sample]
        )

    await msg.answer(ans)


@dp.message(F.text)
async def joke(msg: Message):
    if "штирлиц" in msg.text.lower():
        joke_pos = msg.text.lower().find("штирлиц")
        await msg.answer(
            "<b>ОБНАРУЖЕНА ОТСЫЛКА К АНЕКДОТАМ ПРО ШТИРЛИЦА!!!!</b>\n\n"
            + choice(JOKES),
            reply_parameters=ReplyParameters(
                message_id=msg.message_id,
                chat_id=msg.chat.id,
                quote=msg.text[joke_pos : joke_pos + 7],
                quote_position=joke_pos,
            ),
        )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
