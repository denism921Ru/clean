{\rtf1\ansi\ansicpg1251\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # main.py\
import asyncio\
from datetime import datetime\
from aiogram import Bot, Dispatcher, types, F\
from aiogram.filters import Command\
from aiogram.fsm.context import FSMContext\
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton\
from config import BOT_TOKEN, MANAGER_ID\
from sheets_client import get_sheets\
from states import ShiftStates\
from checklist import CHECKLIST\
\
sheets = get_sheets()\
\
bot = Bot(token=BOT_TOKEN)\
dp = Dispatcher()\
\
start_kb = ReplyKeyboardMarkup(\
    keyboard=[[KeyboardButton(text="\uc0\u9654 \u65039  \u1053 \u1072 \u1095 \u1072 \u1090 \u1100  \u1089 \u1084 \u1077 \u1085 \u1091 ")]],\
    resize_keyboard=True\
)\
\
@dp.message(Command("start"))\
async def cmd_start(message: types.Message, state: FSMContext):\
    await state.set_state(ShiftStates.waiting_for_start)\
    await message.answer("\uc0\u1055 \u1088 \u1080 \u1074 \u1077 \u1090 ! \u1053 \u1072 \u1078 \u1084 \u1080  \'ab\u1053 \u1072 \u1095 \u1072 \u1090 \u1100  \u1089 \u1084 \u1077 \u1085 \u1091 \'bb, \u1095 \u1090 \u1086 \u1073 \u1099  \u1091 \u1074 \u1080 \u1076 \u1077 \u1090 \u1100  \u1089 \u1074 \u1086 \u1080  \u1079 \u1072 \u1103 \u1074 \u1082 \u1080 .", reply_markup=start_kb)\
\
@dp.message(F.text == "\uc0\u9654 \u65039  \u1053 \u1072 \u1095 \u1072 \u1090 \u1100  \u1089 \u1084 \u1077 \u1085 \u1091 ")\
async def start_shift(message: types.Message, state: FSMContext):\
    # \uc0\u1047 \u1076 \u1077 \u1089 \u1100  \u1087 \u1086 \u1082 \u1072  \u1074 \u1099 \u1074 \u1086 \u1076 \u1080 \u1090 \u1089 \u1103  \u1079 \u1072 \u1075 \u1083 \u1091 \u1096 \u1082 \u1072 \
    await message.answer("\uc0\u1057 \u1084 \u1077 \u1085 \u1072  \u1085 \u1072 \u1095 \u1072 \u1090 \u1072 . \u1042  \u1087 \u1086 \u1083 \u1085 \u1086 \u1084  \u1074 \u1072 \u1088 \u1080 \u1072 \u1085 \u1090 \u1077  \u1079 \u1076 \u1077 \u1089 \u1100  \u1073 \u1091 \u1076 \u1091 \u1090  \u1074 \u1072 \u1096 \u1080  \u1079 \u1072 \u1103 \u1074 \u1082 \u1080 .")\
    await state.set_state(ShiftStates.waiting_for_task_start)\
\
# \uc0\u1044 \u1086 \u1073 \u1072 \u1074 \u1100 \u1090 \u1077  \u1086 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082 \u1080  \u1076 \u1083 \u1103  \u1095 \u1077 \u1082 -\u1083 \u1080 \u1089 \u1090 \u1072 , \u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1082 \u1080  \u1092 \u1086 \u1090 \u1086 , \u1079 \u1072 \u1087 \u1080 \u1089 \u1080  \u1074  \u1090 \u1072 \u1073 \u1083 \u1080 \u1094 \u1099  \u1087 \u1086  \u1072 \u1085 \u1072 \u1083 \u1086 \u1075 \u1080 \u1080 \
\
async def main():\
    await dp.start_polling(bot)\
\
if __name__ == "__main__":\
    asyncio.run(main())\
}