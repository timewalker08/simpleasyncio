import asyncio
from datetime import datetime


async def say_after(delay, what):
    print("start at: " + str(datetime.now()))
    await asyncio.sleep(delay)
    print(what + " " + str(datetime.now()))

async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    await asyncio.sleep(4)

asyncio.run(main())
