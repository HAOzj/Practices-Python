import queue
import threading
import time


def producer(q: queue.Queue):
    for i in range(10):
        q.put(i)

def consumer(q: queue.Queue):
    while True:
        # q.get会阻塞,也就是 有就做,没有就歇着
        # 而list需要while来检查,浪费cpu
        item = q.get()
        do(item)
        q.task_done()

def do(ele):
    time.sleep(2)
    print(ele)

q = queue.Queue()

# 创建两个线程
# daemon表示主线程结束,我就结束
t1 = threading.Thread(
    target=consumer, args=(q,)
    , daemon=True
)

t2 = threading.Thread(
    target=consumer, args=(q,)
    , daemon=True
)

t1.start()
t2.start()

# 没有后面代码则什么也不print就结束了,因为主线程已经结束了
producer(q)

# 如果注释掉,则只print0-7就结束进程了,因为8和9任务领完还没来得及done
# 为了保证任务都完成,我们使用q.task_done和q.join
# while not q.empty():
#     time.sleep(1)

# q会阻塞在这里,直到put和task_done一样多
# queue的计数为0则停止
# task_done会计数-1
#q.join()