"""
MIT License

Copyright (c) 2022 BROTHERHOOD COUNCIL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# ""DEAR PRO PEOPLE,  IF YOU REMOVE & CHANGE THIS LINE KINDLY INFORM US AT @TBH_COUNCIL_SUPPORT
# TG :- @THE_BROTHERHOOD_COUNCIL
#     MY ALL BOTS :- BROTHERHOOD_BOTS
#     GITHUB :- THE-BROTHERHOOD-COUNCIL ""

import html
import re
from typing import Optional

from telegram import (
    Bot,
    CallbackQuery,
    Chat,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler
from telegram.utils.helpers import mention_html

from Edith import LOGGER, TIGERS, dispatcher
from Edith.modules.helper_funcs.chat_status import (
    bot_admin,
    can_restrict,
    connection_status,
    is_user_admin,
    user_admin,
    user_admin_no_reply,
)
from Edith.modules.helper_funcs.extraction import extract_user_and_text
from Edith.modules.helper_funcs.string_handling import extract_time
from Edith.modules.log_channel import loggable
from Edith.modules.sql.approve_sql import is_approved


def check_user(user_id: int, bot: Bot, chat: Chat) -> Optional[str]:

    if not user_id:
        reply = "???????????? ????????'??? s????????? ?????? ????? ???????????????????? ?????? ??? ???s????? ????? ???????? ID s????????????????????? ??s ???????????????????????.."
        return reply

    if is_approved(chat.id, user_id):
        reply = (
            "???????s ??s ???s????? is ??????????????????????? ???? ???????s ??????????? ???????? ??????????????????????? ???s?????s ????????'??? ????? ???????????????!"
        )
        return reply

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            reply = "I can't seem to find this user"
            return reply
        raise

    if user_id == bot.id:
        reply = "I'm ???????? ???????????? ???????????? ?????s???????, ???????????"
        return reply

    if is_user_admin(chat, user_id, member) or user_id in TIGERS:
        reply = "????????'???. ????????? s????????????????? ?????s??? ?????? ???????????? ???????? ???????? ???????s ????????."
        return reply

    return None


@connection_status
@bot_admin
@user_admin
@loggable
def mute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    if reply := check_user(user_id, bot, chat):
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#????????????\n"
        f"<b>?????????????:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>???s?????:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    if reason:
        log += f"\n<b>????????s?????:</b> {reason}"

    if member.can_send_messages is None or member.can_send_messages:
        chat_permissions = ChatPermissions(can_send_messages=False)
        bot.restrict_chat_member(chat.id, user_id, chat_permissions)
        msg = (
            f"<code>???????</code><b>???????????? Event</b>\n"
            f"<code> </code><b>??? ??????????????? ???s?????:</b> {mention_html(member.user.id, member.user.first_name)}"
        )
        if reason:
            msg += f"\n<code> </code><b>??? ????????s?????:</b> \n{html.escape(reason)}"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "?????????????????", callback_data=f"unmute_({member.user.id})"
                    )
                ]
            ]
        )

        bot.sendMessage(
            chat.id,
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
        return log
    message.reply_text("???????s ???s????? ??s ?????????????????? ???????????????!")

    return ""


@connection_status
@bot_admin
@user_admin
@loggable
def unmute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text(
            "????????'???? ??????????? to ??????????????? ?????????? ?????? ??? ???s???????????????? ?????? ?????????????????, ????? ???????????? ?????? s????????????????? ?????? ????? ????????????????????."
        )
        return ""

    member = chat.get_member(int(user_id))

    if member.status in ("kicked", "left"):
        message.reply_text(
            "???????s ???s????? ??s??'??? ??????????? ???? ???????? ???????????, ???????????????????? ??????????? ????????'??? ???????????? ??????????? ??????????? ??????????? ?????????? ?????????? "
            "?????????????????? ??????!",
        )

    elif (
        member.can_send_messages
        and member.can_send_media_messages
        and member.can_send_other_messages
        and member.can_add_web_page_previews
    ):
        message.reply_text("???????s ???s????? ?????????????????? ?????s ???????? ??????????? ?????? s????????????.")
    else:
        chat_permissions = ChatPermissions(
            can_send_messages=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_send_polls=True,
            can_change_info=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        try:
            bot.restrict_chat_member(chat.id, int(user_id), chat_permissions)
        except BadRequest:
            pass
        bot.sendMessage(
            chat.id,
            f"{mention_html(member.user.id, member.user.first_name)} ??????s ???????????????????? ???? {mention_html(user.id, user.first_name)} in <b>{message.chat.title}</b>\n<b>????????s?????</b>: <code>{reason}</code>",
            parse_mode=ParseMode.HTML,
        )

        return (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#?????????????????\n"
            f"<b>?????????????:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>???s?????:</b> {mention_html(member.user.id, member.user.first_name)}"
        )
    return ""


@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(update: Update, context: CallbackContext) -> str:
    bot, args = context.bot, context.args
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    user_id, reason = extract_user_and_text(message, args)
    if reply := check_user(user_id, bot, chat):
        message.reply_text(reply)
        return ""

    member = chat.get_member(user_id)

    if not reason:
        message.reply_text("???????? ?????????????'??? s????????????????????? ??? ??????????? ?????? ???????????? ???????s ???s????? ???????!")
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#???????????? ???????????????\n"
        f"<b>?????????????:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>???s?????:</b> {mention_html(member.user.id, member.user.first_name)}\n"
        f"<b>???????????:</b> {time_val}"
    )
    if reason:
        log += f"\n<b>????????s?????:</b> {reason}"

    try:
        if member.can_send_messages is None or member.can_send_messages:
            chat_permissions = ChatPermissions(can_send_messages=False)
            bot.restrict_chat_member(
                chat.id,
                user_id,
                chat_permissions,
                until_date=mutetime,
            )
            msg = (
                f"<code>???????</code><b>??????????? ???????????? ??????????????</b>\n"
                f"<code> </code><b>??? ??????????????? ???s?????:</b> {mention_html(member.user.id, member.user.first_name)}\n"
                f"<code> </code><b>??? ???s????? ????????? ????? ??????????????? ???????:</b> {time_val}\n"
            )

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "?????????????????",
                            callback_data=f"unmute_({member.user.id})",
                        )
                    ]
                ]
            )

            bot.sendMessage(
                chat.id, msg, reply_markup=keyboard, parse_mode=ParseMode.HTML
            )

            return log
        message.reply_text("???????s ???s????? ??s ?????????????????? ???????????????.")

    except BadRequest as excp:
        if excp.message == "???????????? ??????ss???????? ???????? ?????????????":
            # Do not reply
            message.reply_text(f"??????????????? ??????? {time_val}!", quote=False)
            return log
        LOGGER.warning(update)
        LOGGER.exception(
            "???????????? ??????????????? ???s????? %s ???? ??????????? %s (%s) ????????? ?????? %s",
            user_id,
            chat.title,
            chat.id,
            excp.message,
        )
        message.reply_text("?????????? ???????????, ?? ????????'??? ???????????? ??????????? ???s?????.")

    return ""


@user_admin_no_reply
@bot_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    bot: Optional[Bot] = context.bot
    if match := re.match(r"unmute_\((.+?)\)", query.data):
        user_id = match[1]
        chat: Optional[Chat] = update.effective_chat
        member = chat.get_member(user_id)
        chat_permissions = ChatPermissions(
            can_send_messages=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_send_polls=True,
            can_change_info=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        if unmuted := bot.restrict_chat_member(chat.id, int(user_id), chat_permissions):
            update.effective_message.edit_text(
                f"????????????? {mention_html(user.id, user.first_name)} ???????????????????? {mention_html(member.user.id, member.user.first_name)}!",
                parse_mode=ParseMode.HTML,
            )
            query.answer("????????????????????!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#?????????????????\n"
                f"<b>?????????????:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>???s?????:</b> {mention_html(member.user.id, member.user.first_name)}"
            )
    else:
        update.effective_message.edit_text(
            "???????s ???s????? ??s ???????? ??????????????? ????? ?????s ?????????? ???????? ?????????????!"
        )
        return ""


MUTE_HANDLER = CommandHandler("mute", mute, run_async=True)
UNMUTE_HANDLER = CommandHandler("unmute", unmute, run_async=True)
TEMPMUTE_HANDLER = CommandHandler(["tmute", "tempmute"], temp_mute, run_async=True)
UNMUTE_BUTTON_HANDLER = CallbackQueryHandler(button, pattern=r"unmute_")

dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)
dispatcher.add_handler(UNMUTE_BUTTON_HANDLER)

__mod_name__ = "???????????????"
__handlers__ = [MUTE_HANDLER, UNMUTE_HANDLER, TEMPMUTE_HANDLER]
