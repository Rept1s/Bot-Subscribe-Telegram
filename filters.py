from aiogram.types import Message
from aiogram.filters import BaseFilter


class FilterChatType(BaseFilter):
    """
        Проверяет, является ли чат группой/супергруппой.
    """
    async def __call__(self, event: Message) -> bool:
        if event.chat.type == 'group' or event.chat.type == 'supergroup':
            return True
        else:
            await event.answer('Бот предназначен только для групп.')
            return False


class FilterChatAdmin(BaseFilter):
    """
        Проверяет, является ли пользователь администратором.
    """
    async def __call__(self, event: Message) -> bool:
        if event.from_user.id in event.chat.get_administrators():
            return False
        else:
            return True


class FilterSenderAnonim(BaseFilter):
    """
        Проверяет, отправляет ли пользователь сообщения от имени канала/чата.
    """
    async def __call__(self, event: Message) -> bool:
        if event.sender_chat is not None:
            if event.chat.id == event.sender_chat.id:
                return False
            elif event.sender_chat.type in ('channel', 'group', 'supergroup'):
                print('Написал пользователь от имени канала или чата ' + str(event.sender_chat.id) + ' '
                      + str(event.sender_chat.type) + ' @' + str(event.sender_chat.username))
                await event.bot.delete_message(event.chat.id, event.message_id)
                return False
        else:
            return True
