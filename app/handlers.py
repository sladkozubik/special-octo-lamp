import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto

import app.keyboards as kb
from aiogram import F
from aiogram.types import Message, CallbackQuery

from app.logic import create_questions, find_iso

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer('123', reply_markup=kb.start_kb)


@ router.message(Command('flag'))
async def handle_flag(message: Message, state: FSMContext):
    answer, countries = create_questions()
    await state.update_data(correct=answer)
    flag_path = find_iso(answer[0])

    photo = FSInputFile(flag_path)

    await message.answer_photo(photo,
                               reply_markup=kb.create_question(countries)
                               )


@router.callback_query(F.data.startswith('answer_'))
async def check_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    correct = data['correct']
    user_answer = callback.data.split('_')[1]

    if user_answer == correct[0]:
        text = f'✅, Это {correct[1]}!'
    else:
        text = f"❌ Это {correct[1]}"
    await callback.message.edit_caption(
        caption=text,
    )
    await asyncio.sleep(1)
    answer, countries = create_questions()
    await state.update_data(correct=answer)
    new_flag = find_iso(answer[0])
    photo = FSInputFile(new_flag)

    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo),
        reply_markup=kb.create_question(countries)
    )

    await callback.answer()
