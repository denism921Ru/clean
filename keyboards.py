from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Квартиры", callback_data="admin:apartments")],
            [InlineKeyboardButton(text="🧾 Задачи", callback_data="admin:tasks")],
            [InlineKeyboardButton(text="➕ Создать задачу", callback_data="admin:create_task")],
        ]
    )


def admin_apartments_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить квартиру", callback_data="admin:add_apartment")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:back")],
        ]
    )


def back_to_admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:back")]]
    )


def apartments_pick_kb(apartments: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for a in apartments:
        rows.append(
            [InlineKeyboardButton(text=f"🏠 {a.get('name','')} — {a.get('address','')}", callback_data=f"pick_apartment:{a.get('id')}")]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def housekeepers_pick_kb(housekeepers: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for u in housekeepers:
        tg_id = u.get("tg_id") or u.get("id") or ""
        nm = u.get("name") or tg_id
        rows.append(
            [InlineKeyboardButton(text=f"🧑‍🔧 {nm} ({tg_id})", callback_data=f"pick_housekeeper:{tg_id}")]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def hk_tasks_kb(tasks: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for t in tasks:
        tid = t.get("id")
        addr = t.get("apartment_address", "")
        tm = t.get("time", "")
        st = t.get("status", "")
        rows.append([InlineKeyboardButton(text=f"🧹 {tm} — {addr} ({st})", callback_data=f"hk:task:{tid}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def hk_task_actions_kb(task_id: str, status: str) -> InlineKeyboardMarkup:
    buttons = []
    if status in ("ASSIGNED", ""):
        buttons.append([InlineKeyboardButton(text="▶️ Начать (с фото)", callback_data=f"hk:start:{task_id}")])
    if status in ("IN_PROGRESS",):
        buttons.append([InlineKeyboardButton(text="✅ Завершить (с фото)", callback_data=f"hk:finish:{task_id}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="hk:tasks")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
