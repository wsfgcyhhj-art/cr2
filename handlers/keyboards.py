from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Каталог")],
    [KeyboardButton(text="Корзина"), KeyboardButton(text="Контакты")]
])

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg")],
    [InlineKeyboardButton(text="Начать игру", callback_data="quiz_start")]
])

# Редактировать = edit:101

def product_actions(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'edit:{product_id}'),
             InlineKeyboardButton(text="🗑 Удалить", callback_data=f'delete:{product_id}')]
        ]
    )


edit_fields = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Название', callback_data='field_name'), 
         InlineKeyboardButton(text='Цена', callback_data='field_price'), 
         InlineKeyboardButton(text='Описание', callback_data='field_description'),
         InlineKeyboardButton(text='Категория', callback_data='field_category'),
         InlineKeyboardButton(text="Цвет", callback_data='field_color')
         ]
    ]
)