import asyncio
import time


async def task(delay: int, msg: str):
    await asyncio.sleep(delay)
    print(msg)
    print(time.strftime('%X'))
    return f"{msg} - {delay}"


async def main():
    # create_task把coroutine变成task
    # 并把task注册到event loop
    # 不过控制权还是在main中
    task1 = asyncio.create_task(task(2, "hello"))
    task2 = asyncio.create_task(task(1, "world"))

    print(f"main start at {time.strftime('%X')}")

    # await表示需要把这个task完成
    # 返回后控制权交还给event loop
    ret1 = await task1
    ret2 = await task2

    print(f"main done at {time.strftime('%X')}")


asyncio.run(main())