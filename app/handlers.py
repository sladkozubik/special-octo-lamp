import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto
from app.sfms import Game
import app.keyboards as kb
from aiogram import F
from aiogram.types import Message, CallbackQuery

from app.logic import create_questions, find_iso

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer('123', reply_markup=kb.start_kb)


@router.message(Command('flag'))
async def handle_flag(message: Message, state: FSMContext):
    # answer, countries = create_questions()
    await state.set_state(Game.continent)

    await message.answer('Выбирите континент', reply_markup=kb.kb_continents)


@router.callback_query(Game.continent, F.data.startswith('continent:'))
async def handle_continent(callback: CallbackQuery, state: FSMContext):
    continent = callback.data.split(':')[1]
    if continent == 'Мир':
        answer, countries = create_questions()
    else:
        answer, countries = create_questions(continent=continent)
    await state.update_data(continent=continent,
                            correct=answer)

    photo = FSInputFile(find_iso(answer[0]))

    await callback.message.answer_photo(photo, reply_markup=kb.create_question(countries)
                                        )
    await callback.answer()


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
    continent = data['continent']
    if continent == 'Мир':
        answer, countries = create_questions()
    else:
        answer, countries = create_questions(continent)
    await state.update_data(correct=answer)
    new_flag = find_iso(answer[0])
    photo = FSInputFile(new_flag)

    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo),
        reply_markup=kb.create_question(countries)
    )

    await callback.answer()
