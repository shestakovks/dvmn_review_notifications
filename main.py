import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger("LongPollingApp")

DVMN_BASE_URL = "https://dvmn.org"
LONG_POLLING_URL = "https://dvmn.org/api/long_polling/"
DEFAULT_LONG_POLLING_TIMEOUT = 90


class BotLogsHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, telegram_token=None, proxy_url=None, chat_id=None):
        self.bot = setup_telegram_bot(telegram_token, proxy_url)
        self.chat_id = chat_id
        super(BotLogsHandler, self).__init__(level=level)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


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
            response.raise_for_status()
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
            logger.info(f"Next request will be sent in {timeout} second(s).")
            time.sleep(timeout)
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP Error occurred: {err}.")
            raise


def main():
    # Get parameters for our app
    load_dotenv()
    telegram_notify_bot_token = os.getenv("TELEGRAM_NOTIFY_BOT_TOKEN")
    telegram_log_bot_token = os.getenv("TELEGRAM_LOG_BOT_TOKEN")
    proxy_url = os.getenv("TELEGRAM_PROXY_URL", None)
    dvmn_api_token = os.getenv("DVMN_API_TOKEN")
    timeout = int(os.getenv("DVMN_LONG_POLLING_TIMEOUT", DEFAULT_LONG_POLLING_TIMEOUT))
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # Setup logger
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    bot_handler = BotLogsHandler(level=logging.INFO, telegram_token=telegram_log_bot_token,
                                 proxy_url=proxy_url, chat_id=chat_id)
    bot_handler.setFormatter(formatter)
    logger.addHandler(bot_handler)

    # Setup bot and start polling
    while True:
        try:
            notification_bot = setup_telegram_bot(telegram_notify_bot_token, proxy_url)
            poll_for_new_reviews(dvmn_api_token, notification_bot, chat_id, timeout)
        except Exception as err:
            logger.error("Unexpected error occurred:")
            logger.error(err, exc_info=True)
            logger.info(f"Bot will restart in 120 seconds.")
            time.sleep(120)


if __name__ == '__main__':
    main()
