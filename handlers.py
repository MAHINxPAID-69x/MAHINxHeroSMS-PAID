import asyncio
import html
import json
import logging
import re
import time
from datetime import datetime, timezone
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from aiohttp import web
from api_client import HeroSMSClient, check_telegram_numbers
import database as db
import keyboards as kb
from states import BotStates

router = Router()
global_bot = None

def set_bot_instance(bot):
    global global_bot
    global_bot = bot

def get_bot_instance():
    return global_bot

ADMIN_ID = 7266067201
COLOMBIA_ID = 33
TG_SERVICE = "tg"

# Live Monitoring Telegram Group ID
OTP_LOG_GROUP_ID = -1004477485295

# Defaults
DEFAULT_MAX_PRICE = 0.145
DEFAULT_OPERATOR = "any"
DEFAULT_PREFIXES = ["57319"]

MENU_BUTTONS = [
    "Bulk Buy Numbers",
    "Active Numbers",
    "Balance",
    "Profile",
    "📊 Users & Activity Analytics",
    "⚙️ Buy Config (Operator/Price)",
    "🚫 Manage Excluded Prefixes",
    "📢 Broadcast Message",
    "🚫 Ban / Unban User",
    "❌ Unapprove / Revoke Access",
    "⏳ Extend User Subscription",
    "⚙️ Toggle Maintenance",
    "⚙ Toggle Maintenance",
    "⬅️ Back to User Menu"
]

# --- Verified Custom Premium Emojis ---
EMOJI_USER    = '<tg-emoji emoji-id="5397693616602755866">👤</tg-emoji>'
EMOJI_ID      = '<tg-emoji emoji-id="5289967908309442996">🆔</tg-emoji>'
EMOJI_FLAG    = '<tg-emoji emoji-id="5294010206974397371">🇨🇴</tg-emoji>'
EMOJI_CLOCK   = '<tg-emoji emoji-id="5215394081911351762">⏰</tg-emoji>'
EMOJI_CHART   = '<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji>'
EMOJI_TICK    = '<tg-emoji emoji-id="6087154735125630953">✅</tg-emoji>'
EMOJI_CROSS   = '<tg-emoji emoji-id="5321012601939838274">❌</tg-emoji>'
EMOJI_WARN    = '<tg-emoji emoji-id="5420323339723881652">⚠️</tg-emoji>'
EMOJI_CARD    = '<tg-emoji emoji-id="5206330150433595241">💳</tg-emoji>'
EMOJI_BOX     = '<tg-emoji emoji-id="5298809897352193254">📦</tg-emoji>'
EMOJI_KEY     = '<tg-emoji emoji-id="5193070340850327783">🔑</tg-emoji>'
EMOJI_LOCK    = '<tg-emoji emoji-id="6334379984760604198">🔒</tg-emoji>'
EMOJI_BAN     = '<tg-emoji emoji-id="5280803324273115630">🚫</tg-emoji>'
EMOJI_PLANE   = '<tg-emoji emoji-id="5411563083908797492">🛫</tg-emoji>'
EMOJI_SIREN   = '<tg-emoji emoji-id="5395695537687123235">🚨</tg-emoji>'

# --- In-Memory Speed Cache ---
USER_CACHE = {}
SETTINGS_CACHE = {}

async def get_cached_user(user_id: int):
    if user_id in USER_CACHE:
        return USER_CACHE[user_id]
    user = await db.get_user(user_id)
    if user:
        USER_CACHE[user_id] = user
    return user

def invalidate_user_cache(user_id: int):
    USER_CACHE.pop(user_id, None)

async def get_cached_setting(key: str, default: str = ""):
    if key in SETTINGS_CACHE:
        return SETTINGS_CACHE[key]
    val = await db.get_setting(key)
    if val is None:
        val = default
    SETTINGS_CACHE[key] = val
