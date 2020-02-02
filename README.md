# DVMN review notification telegram bot

Python3 project that long-polling dvmn web-site for any new reviews for your lessons and if there are any - sends you a message via telegram bot.


## How to install

1. First of all you need to register at [dvmn](https://dvmn.org/modules/), if you still haven't.
2. Go to [API](https://dvmn.org/api/docs/) page and find your token, it looks something like this - `7c594b269cdd3562225f076b2861d3eb63454b8b`.
3. Now, you need to register new bot on [Telegram](https://telegram.org/). Find `@BotFather` bot in your app, type `/newbot`, then follow the instructions of that bot. When you're finished, you'll get your bot api token, which looks like this - `95132391:wP3db3301vnrob33BZdb33KwP3db3F1I`.
4. Then you need to type `\start` in your bot's chat.
5. Go to `@myidbot` in Telegram app and type `\getid` to get your chat_id.
6. Now you need to create `.env` file in directory with this program and put there your dvmn api token, telegram bot token and your telegram chat_id. Your can also set long polling timeout and proxy for telegram bot, but its optional. `.env` file should look like this, but with your data instead:
    ```
     DVMN_API_TOKEN=7c594b269cdd3562225f076b2861d3eb63454b8b
     TELEGRAM_BOT_TOKEN=95132391:wP3db3301vnrob33BZdb33KwP3db3F1I
     TELEGRAM_CHAT_ID=123456789
     DVMN_LONG_POLLING_TIMEOUT=90
     TELEGRAM_PROXY_URL=http://161.171.181.11:2255
    ```
7. Python3 should be already installed. The script was made using `Python 3.6.9`. This version or higher should be fine.
8. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
    ```
    pip install -r requirements.txt
    ```

## How to use

```
$ python3 main.py 
```
If some of your lessons are reviewed - you'll get following result - [screenshot](https://imgur.com/X941KEM).
Application is also logging itself into `debug.log` file in the same directory. Logs look like this:
```
2020-02-02 17:04:01,808 - LongPollingApp - DEBUG - Sending GET request with following parameters: params={'timestamp': 1580650527.7589002}, timeout=90
2020-02-02 17:05:32,049 - LongPollingApp - DEBUG - Got following answer: {'request_query': [['timestamp', '1580650527.7589002']], 'status': 'timeout', 'timestamp_to_request': 1580650527.7589002}
2020-02-02 17:05:32,049 - LongPollingApp - DEBUG - Sending GET request with following parameters: params={'timestamp': 1580650527.7589002}, timeout=90
2020-02-02 17:06:40,978 - LongPollingApp - DEBUG - Got following answer: {'request_query': [['timestamp', '1580650527.7589002']], 'status': 'found', 'new_attempts': [{'submitted_at': '2020-02-02T17:06:40.909908+03:00', 'timestamp': 1580652400.909908, 'is_negative': True, 'lesson_title': 'Раскрутите планету', 'lesson_url': '/modules/meeting-python/lesson/rotating-planet/'}], 'last_attempt_timestamp': 1580652400.909908}
2020-02-02 17:06:41,361 - LongPollingApp - DEBUG - Sent message to user.
```

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
