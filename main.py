import logging
import os

import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger("LongPollingApp")

DVMN_BASE_URL = "https://dvmn.org"
LONG_POLLING_URL = "https://dvmn.org/api/long_polling/"
DEFAULT_LONG_POLLING_TIMEOUT = 90


def setup_telegram_bot(telegram_token, proxy_url=None):
    if proxy_url is not None:
        proxy_settings = telegram.utils.request.Request(proxy_url=proxy_url)
        bot = telegram.Bot(token=telegram_token, request=proxy_settings)
    else:
        bot = telegram.Bot(token=telegram_token)
    logger.info("Bot setup complete.")
    return bot


def send_bot_message(bot, chat_id, answer):
    for attempt in answer["new_attempts"]:
        is_negative = attempt["is_negative"]
        lesson_title = attempt["lesson_title"]
        lesson_url = attempt["lesson_url"]
        message = f"У вас проверили работу \"{lesson_title}\" ({DVMN_BASE_URL+lesson_url})!\n"
        if is_negative:
            message += "К сожалению, в работе нашлись ошибки."
        else:
            message += "Преподавателю все понравилось, можно приступать к следующему уроку!"
        bot.send_message(chat_id=chat_id, text=message)
        logger.info("Sent message to user.")


def poll_for_new_reviews(dvmn_api_token, bot, chat_id, timeout):
    headers = {
        "Authorization": f"Token {dvmn_api_token}"
    }
    params = None
    while True:
        try:
            logger.debug(f"Sending GET request with following parameters: "
                         f"params={params}, timeout={timeout}")
            response = requests.get(LONG_POLLING_URL, params=params, headers=headers, timeout=timeout)
            answer = response.json()
            logger.debug(f"Got following answer: {answer}")
            if answer.get("status") == "found":
                send_bot_message(bot, chat_id, answer)
                params = {
                    "timestamp": answer["last_attempt_timestamp"],
                }
            elif answer.get("status") == "timeout":
                params = {
                    "timestamp": answer["timestamp_to_request"],
                }
            else:
                params = None
        except requests.exceptions.ReadTimeout:
            logger.warning("Timeout error occurred.")
        except requests.exceptions.ConnectionError:
            logger.warning("Network error occurred.")


def main():
    # Setup logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("debug.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    proxy_url = os.getenv("TELEGRAM_PROXY_URL", None)
    bot = setup_telegram_bot(telegram_token, proxy_url)

    dvmn_api_token = os.getenv("DVMN_API_TOKEN")
    timeout = int(os.getenv("DVMN_LONG_POLLING_TIMEOUT", DEFAULT_LONG_POLLING_TIMEOUT))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    poll_for_new_reviews(dvmn_api_token, bot, chat_id, timeout)


if __name__ == '__main__':
    main()
