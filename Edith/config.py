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

import json
import os


def get_user_list(config, key):
    with open("{}/Edith/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    LOGGER = True

    API_ID = "983922"
    APP_HASH = "funssnAjsjaSJns82AjajU" 
    ARQ_API_KEY = "TENRCY-KDKSK-MSMSM-OXQYYO-ARQ"
    BOT_ID = "5408158735"
    TOKEN = "5458182410:KINGABISHNOI-UM"
    OWNER_ID = "5331427205"
    OPENWEATHERMAP_ID = "22322"
    OWNER_USERNAME = "hunter_is_back"
    BOT_USERNAME = "Edith_Robot"
    SUPPORT_CHAT = "TEAM_BLACK_SUPPORT"
    UPDATES_CHANNEL = "the_brotherhood_council"
    SUPPORT_CHANNEL = "team_black_sipport"
    JOIN_LOGGER = "-1001497222182"
    EVENT_LOGS = "-1001497222182"
    ERROR_LOGS = "-1001497222182"

    SQLALCHEMY_DATABASE_URI = ""
    DB_URL = ""
    MONGO_DB_URL = ""  # needed for any database modules
    MONGO_URL = ""
    DB_URL2 = ""  # YOUR MONGO_DB_URI
    ARQ_API_URL = "https://arq.hamker.in"
    BOT_API_URL = "https://api.telegram.org/bot"
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None

    REDIS_URL = ""

    DRAGONS = get_user_list("elevated_users.json", "sudos")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    REQUESTER = get_user_list("elevated_users.json", "whitelists")
    DEMONS = get_user_list("elevated_users.json", "supports")
    INSPECTOR = get_user_list("elevated_users.json", "sudos")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    DONATION_LINK = "https://t.me/BLACK_LORD_ON_FIRE"
    CERT_PATH = None
    STRICT_GBAN = "True"
    PORT = ""
    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = 8
    BAN_STICKER = ""
    ALLOW_EXCL = True
    CASH_API_KEY = "NAI H BRO"
    TIME_API_KEY = "HUNTER"
    WALL_API = "F-OFF"
    AI_API_KEY = "HATEYOU"
    BL_CHATS = []
    SPAMMERS = None
    SPAMWATCH_API = ""
    ALLOW_CHATS = None
    TEMP_DOWNLOAD_DIRECTORY = "./"
    HEROKU_APP_NAME = ""
    HEROKU_API_KEY = ""
    REM_BG_API_KEY = "LSdLgCceYz8vNqFgJVzrkDgR"
    LASTFM_API_KEY = "FMLODA"
    CF_API_KEY = "KISS"
    BL_CHATS = []
    MONGO_PORT = "27017"
    MONGO_DB = "Edith"
    PHOTO = "https://te.legra.ph/file/aa3f43c174f03b422aea8.jpg"
    HELP_IMG = "https://te.legra.ph/file/aa3f43c174f03b422aea8.jpg"
    START_IMG = "https://te.legra.ph/file/aa3f43c174f03b422aea8.jpg"
    TIME_API_KEY = "5LB4TAKPEKZ0"
    INFOPIC = False
    GENIUS_API_TOKEN = "28jwoKAkskaSjsnsksAjnwjUJwj"


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True


# ENJOY
