import asyncio
from environs import Env
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
album_end_tracker = {}


async def delete_start_func(message: Message):
    """
        Удаление сообщения пользователя и запуск остальных функций.
    """
    if not await user_is_subscriber(message.bot, message.from_user.id, Env().str("CHANNEL_ID")):
        await message.delete()
        if await check_album(message) is False:
            await answer_message(message)


async def user_is_subscriber(bot, user_id: int, channel_id: str) -> bool:
    """
        Проверяет, подписан ли пользователь на канал.
    """
    try:
        member_status = await bot.get_chat_member(channel_id, user_id)
        return member_status.status not in ["left", "kicked"]
    except Exception as e:
        print(f"Ошибка при проверке статуса подписки: {e}")
        return False


async def check_album(message: Message):
    """
        Проверяет, является ли альбомом, для того, чтобы в дальнейшем не дублировать сообщение с просьбой подписаться.
    """
    if message.media_group_id:
        if message.media_group_id not in album_end_tracker:
            album_end_tracker[message.media_group_id] = message.message_id
        else:
            album_end_tracker[message.media_group_id] = max(album_end_tracker[message.media_group_id],
                                                            message.message_id)

        await asyncio.sleep(4)  # Ожидание, для получения всего альбома
        if album_end_tracker[message.media_group_id] == message.message_id:
            await answer_message(message)
            del album_end_tracker[message.media_group_id]
    else:
        return False


async def first_name(message: Message):
    """
        Проверяет на наличие имени/юзернейма для дальнейшего обращения по имени/юзернейму.
    """
    if message.from_user.first_name or message.from_user.full_name or message.from_user.username is not None:
        return (message.from_user.first_name + ',' or message.from_user.full_name + ','
                or message.from_user.username + ',')
    else:
        return 'Дорогой пользователь!'


async def answer_message(message: Message):
    """
        Просьба подписаться на канал с дальнейшим удалением сообщения от бота.
    """
    send_answer = await message.answer(
        '<a href="tg://user?id=' + str(message.from_user.id) + '">' + str(await first_name(message)) + '</a>' +
        "\nПожалуйста, подпишитесь на канал, чтобы писать сообщения в этот чат.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
            text="Подписаться на канал", url=Env().str("INVITE_LINK"))]]))
    await asyncio.sleep(180)  # 3 минут ожидания, далее очистка для удаления лишнего спама
    await send_answer.delete()
