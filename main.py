#!/usr/bin/env python3

"""
main.py
Usage: 
1. First, activate virtual environment with command:
    "source .venv/bin/activate "
2. Create a .env file and fill in this info:
    TG_API_KEY=
    CMC_API_KEY=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DEBUG=
2. Then, start the telegram bot with "./main.py". 
2a. If permission denied, run this command first "chmod +x main.py".
3. Message your Telegram bot /help to see how to interact with it!
"""

from bot.bot import create_bot
import asyncio
from querier import start_query_loop, result_queue
from check_condition import check_condition
from threading import Thread

def start_polling_in_thread(bot):
    # Start polling in a separate thread
    bot.polling(none_stop=True)

async def main():
    bot = create_bot()

    # Start the bot's polling method in a separate thread
    polling_thread = Thread(target=start_polling_in_thread, args=(bot,))
    polling_thread.start()

    # # Start the query loop
    # query_task = asyncio.create_task(start_query_loop())

    # while True:
    #     # wait for results from query loop
    #     resulting_statistic, notif_id = await result_queue.get()
    #     # check if the results meet the condition
    #     if check_condition(resulting_statistic, notif_id):
    #         print("send message to owner of that notif_id!")
    # Keep the main coroutine running indefinitely
    while True:
        await asyncio.sleep(1)  # Sleep for a short time to prevent high CPU usage


if __name__ == '__main__':
    asyncio.run(main())

