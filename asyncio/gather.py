import asyncio
import time


async def task(delay: int, msg: str):
    await asyncio.sleep(delay)
    print(msg, time.strftime('%X'))
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
    print(f"rets are {ret1} and {ret2}")
    print(f"main done at {time.strftime('%X')}")


async  def main2():
    print(f"main2 start at {time.strftime('%X')}")

    # 为了避免过多任务一个个create_task和await
    # 使用gather
    # gather返回一个future
    # gather中可以是coroutine | task | gather
    ret = await asyncio.gather(
        task(2, "hello"),
        task(1, "wrold")
    )
    print(f"rets are {ret}")
    print(f"main2 done at {time.strftime('%X')}")

# 是一个object,类似于生成器,并不会执行
xixi = task(3, "hello world")

asyncio.run(main())
asyncio.run(main2())