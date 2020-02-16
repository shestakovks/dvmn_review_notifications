# DVMN review notification telegram bot

Python3 project that long-polling dvmn web-site for any new reviews for your lessons and if there are any - sends you a message via telegram bot.


## How to install

1. First of all you need to register at [dvmn](https://dvmn.org/modules/), if you still haven't.
2. Go to [API](https://dvmn.org/api/docs/) page and find your token, it looks something like this - `7c594b269cdd3562225f076b2861d3eb63454b8b`.
3. Now, you need to register two new bots on [Telegram](https://telegram.org/). Find `@BotFather` bot in your app, type `/newbot`, then follow the instructions of that bot. When you're finished, you'll get your bot api token, which looks like this - `95132391:wP3db3301vnrob33BZdb33KwP3db3F1I`. Create two bots, you'll use one as a notifying bot and other as a logging bot.
4. Then you need to type `\start` in your bots chats.
5. Go to `@myidbot` in Telegram app and type `\getid` to get your chat_id.
6. Now you have a choice - run bot locally (follow 6.1) or deploy bot on heroku (follow 6.2).

    6.1. This chapter will cover local deploy.
    - You need to create `.env` file in directory with this program and put there your dvmn api token, telegram bot tokens and your telegram chat_id. Your can also set long polling timeout and proxy for telegram bot, but its optional. `.env` file should look like this, but with your data instead:
        ```
         DVMN_API_TOKEN=7c594b269cdd3562225f076b2861d3eb63454b8b
         TELEGRAM_NOTIFY_BOT_TOKEN=95132391:wP3db3301vnrob33BZdb33KwP3db3F1I
         TELEGRAM_LOG_BOT_TOKEN=1066971237:EEA323drwZN7TXRiPHdrAgs7zwcntHxgkg
         TELEGRAM_CHAT_ID=123456789
         DVMN_LONG_POLLING_TIMEOUT=90
         TELEGRAM_PROXY_URL=http://161.171.181.11:2255
        ```
    - Python3 should be already installed. The script was made using `Python 3.6.9`. This version or higher should be fine.
    - Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
        ```
        pip install -r requirements.txt
        ```

    6.2. This chapter will cover Heroku deploy.
    
    - Register on [Heroku](https://www.heroku.com/). Connect your Heroku account to your GitHub account. Fork current repository to your account.
    - Create new app on [Heroku's Apps page](https://dashboard.heroku.com/apps).
    - Go to "Deploy" tab of your app and deploy `master` branch of the forked repository.
    - Go to "Settings" tab of your app and add your api keys and tokens into "Config Vars" section (for vars name reference, see 6.1).


## How to use

1. Locally
    ```
    $ python3 main.py 
    ```
2. Heroku

    Go to "Resources" tab of your app and turn on your bot.
    
Results:

If some of your lessons are reviewed - you'll get following result - [screenshot](https://imgur.com/X941KEM).
Application is also logging itself into another bot. Logging bot look like this - [screenshot](https://imgur.com/Q23A5ot).

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
