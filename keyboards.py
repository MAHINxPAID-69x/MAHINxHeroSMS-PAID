from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    CopyTextButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# --- Pure Telegram Premium Emoji IDs (No standard unicode fallback text) ---
PEM_ROCKET  = "5352597830089347330"  # 🚀 (Bulk Buy / High Speed Turbo)
PEM_OK      = "6111726981760423576"  # ✅ (Success / Done / Active)
PEM_NO      = "6311965254817423602"  # ❌ (Danger / Cancel / Reject)
PEM_WARN    = "6314510813214284503"  # ⚠️ (Alert)
PEM_ADMIN   = "5353032893096567467"  # 📊 (Analytics / Stats)
PEM_USER    = "5352861489541714456"  # 👤 (Profile / Account)
PEM_MONEY   = "6111799373434197692"  # 💸 (Balance / Money / USD)
PEM_GIFT    = "6109561463544747928"  # 🎁 (Bonus)
PEM_MSG     = "5337302974806922068"  # 💬 (Broadcast)
PEM_PIN     = "6111410240807245099"  # 📌 (Pinned Task)
PEM_ADD     = "6188038822509418008"  # ➕ (Add / Insert)
PEM_REM     = "6188343249791358585"  # ➖ (Remove / Sub)
PEM_VIEW    = "5386367538735104399"  # 👀 (View / Eye)
PEM_KEY     = "6233302765582424442"  # 🔑 (API Key / Auth)
PEM_WAIT    = "6233136657722251031"  # ⏳ (Clock / Duration)
PEM_EARN    = "6186175669991379791"  # 🤑 (Profit / Rates)
PEM_BELL    = "6260082445018731350"  # 🔔 (Alert Bell)
PEM_CROWN   = "6183661284467152997"  # 👑 (Owner / VIP)
PEM_GEAR    = "6260111633616475361"  # ⚙️ (Settings / Config)
PEM_GROUP   = "6233527959307688784"  # 👥 (Users / Community)
PEM_TARGET  = "6109432142079466939"  # 🎯 (Target Operator / Direct)


def main_reply_menu() -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text="Bulk Buy Numbers", icon_custom_emoji_id=PEM_ROCKET, style="success")
    b.button(text="Active Numbers", icon_custom_emoji_id=PEM_VIEW, style="primary")
    b.button(text="Balance", icon_custom_emoji_id=PEM_MONEY, style="success")
    b.button(text="Profile", icon_custom_emoji_id=PEM_USER, style="primary")
    b.adjust(2, 2)
    return b.as_markup(resize_keyboard=True)


def admin_reply_menu(restock_on: bool = True) -> ReplyKeyboardMarkup:
    restock_label = "Restock Alert: ON" if restock_on else "Restock Alert: OFF"
    b = ReplyKeyboardBuilder()
    b.button(text="Users & OTP Monitor", icon_custom_emoji_id=PEM_ADMIN, style="primary")
    b.button(text="Daily & Lifetime Stats", icon_custom_emoji_id=PEM_EARN, style="primary")
    b.button(text="Live Active Users", icon_custom_emoji_id=PEM_GROUP, style="success")
    b.button(text="Buy Config (Operator/Price)", icon_custom_emoji_id=PEM_GEAR, style="primary")
    b.button(text="Manage Excluded Prefixes", icon_custom_emoji_id=PEM_REM, style="primary")
    b.button(text="Broadcast Message", icon_custom_emoji_id=PEM_MSG, style="primary")
    b.button(text="Ban / Unban User", icon_custom_emoji_id=PEM_NO, style="danger")
    b.button(text="Unapprove / Revoke Access", icon_custom_emoji_id=PEM_NO, style="danger")
    b.button(text="Extend User Subscription", icon_custom_emoji_id=PEM_WAIT, style="success")
    b.button(text=restock_label, icon_custom_emoji_id=PEM_BELL, style="success" if restock_on else "danger")
    b.button(text="Toggle Maintenance", icon_custom_emoji_id=PEM_WARN, style="danger")
    b.button(text="Back to User Menu", icon_custom_emoji_id=PEM_ROCKET, style="primary")
    b.adjust(2, 2, 2, 2, 2, 1, 1)
    return b.as_markup(resize_keyboard=True)


def admin_config_menu(current_op: str, current_price: float) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=f"Operator: {current_op.upper()}", callback_data="cfg_set_operator", icon_custom_emoji_id=PEM_TARGET, style="primary")
    b.button(text=f"Max Price: ${current_price:.3f}", callback_data="cfg_set_price", icon_custom_emoji_id=PEM_MONEY, style="primary")
    b.button(text="Set Any Operator", callback_data="cfg_op_any", icon_custom_emoji_id=PEM_OK, style="success")
    b.button(text="Set Claro Only", callback_data="cfg_op_claro", icon_custom_emoji_id=PEM_OK, style="success")
    b.button(text="Set Movistar Only", callback_data="cfg_op_movistar", icon_custom_emoji_id=PEM_OK, style="success")
    b.button(text="Set Tigo Only", callback_data="cfg_op_tigo", icon_custom_emoji_id=PEM_OK, style="success")
    b.button(text="Back", callback_data="menu_admin_close", icon_custom_emoji_id=PEM_NO, style="danger")
    b.adjust(2, 2, 2, 1)
    return b.as_markup()


def prefix_manage_menu() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Add Prefix", callback_data="pfx_add", icon_custom_emoji_id=PEM_ADD, style="success")
    b.button(text="Remove Prefix", callback_data="pfx_remove", icon_custom_emoji_id=PEM_REM, style="primary")
    b.button(text="Clear All", callback_data="pfx_clear_all", icon_custom_emoji_id=PEM_NO, style="danger")
    b.button(text="View All", callback_data="pfx_view", icon_custom_emoji_id=PEM_VIEW, style="primary")
    b.button(text="Back", callback_data="menu_admin_close", icon_custom_emoji_id=PEM_ROCKET, style="primary")
    b.adjust(2, 2, 1)
    return b.as_markup()


def profile_menu() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Change API Key", callback_data="profile_change_key", icon_custom_emoji_id=PEM_KEY, style="primary")
    b.button(text="Back", callback_data="menu_main", icon_custom_emoji_id=PEM_ROCKET, style="primary")
    b.adjust(1)
    return b.as_markup()


def back_button(callback_data: str = "menu_main") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Back", callback_data=callback_data, icon_custom_emoji_id=PEM_ROCKET, style="primary")
    return b.as_markup()


def number_action_menu(activation_id: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Refresh OTP", callback_data=f"refresh_{activation_id}", icon_custom_emoji_id=PEM_WAIT, style="success")
    b.button(text="Cancel Number", callback_data=f"single_cancel_{activation_id}", icon_custom_emoji_id=PEM_NO, style="danger")
    b.adjust(2)
    return b.as_markup()


def active_numbers_menu(activations: list) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for act in activations:
        aid = str(act.get("activationId", ""))
        phone = str(act.get("phoneNumber", "Unknown"))
        if aid:
            b.button(text=f"Cancel +{phone}", callback_data=f"active_cancel_{aid}", icon_custom_emoji_id=PEM_NO, style="danger")

    b.button(text="Cancel All Active", callback_data="cancel_all_active", icon_custom_emoji_id=PEM_NO, style="danger")
    b.button(text="Back", callback_data="menu_main", icon_custom_emoji_id=PEM_ROCKET, style="primary")
    b.adjust(1)
    return b.as_markup()


def otp_copy_menu(otp_code: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    code_str = str(otp_code).strip()
    try:
        b.row(
            InlineKeyboardButton(
                text=code_str,
                copy_text=CopyTextButton(text=code_str),
                icon_custom_emoji_id=PEM_OK,
                style="success"
            )
        )
    except Exception:
        b.button(text=code_str, callback_data="noop", icon_custom_emoji_id=PEM_OK, style="success")
    return b.as_markup()


def bulk_report_menu(batch_id: str, show_only_fresh: bool = False) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if not show_only_fresh:
        b.button(text="View Only Fresh", callback_data=f"filter_fresh_{batch_id}", icon_custom_emoji_id=PEM_OK, style="success")
    else:
        b.button(text="Show All", callback_data=f"filter_all_{batch_id}", icon_custom_emoji_id=PEM_VIEW, style="primary")
    b.adjust(1)
    return b.as_markup()


def approval_duration_menu(user_id: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="1 Day", callback_data=f"appr_{user_id}_1", icon_custom_emoji_id=PEM_WAIT, style="primary")
    b.button(text="3 Days", callback_data=f"appr_{user_id}_3", icon_custom_emoji_id=PEM_WAIT, style="primary")
    b.button(text="7 Days", callback_data=f"appr_{user_id}_7", icon_custom_emoji_id=PEM_WAIT, style="primary")
    b.button(text="30 Days", callback_data=f"appr_{user_id}_30", icon_custom_emoji_id=PEM_WAIT, style="primary")
    b.button(text="Lifetime", callback_data=f"appr_{user_id}_life", icon_custom_emoji_id=PEM_CROWN, style="success")
    b.button(text="Reject", callback_data=f"appr_{user_id}_reject", icon_custom_emoji_id=PEM_NO, style="danger")
    b.adjust(2, 3, 1)
    return b.as_markup()
