from random import randint
import simpy
from pprint import pprint

itemcount = 0
env = simpy.Environment()

res = simpy.Resource(env, 1)
res1 = simpy.Resource(env, 1)
log = []

class Item:
    def __init__(self, i) -> None:
        self.id = i
        self.count = 0

    def change(self, time):
        self.count = time

def pro(i: Item) :
    log.append([env.now, i.id, None, len(res.queue), "IN -> 0"])
    with res.request() as req:
        yield req
        timecount = randint(5, 8)
        yield env.timeout(timecount)
        log.append([env.now, i.id, timecount, len(res.queue), "OUT -> 0"])
        i.change(timecount)
    yield env.process(pro1(i))


def pro1(i: Item) :
    log.append([env.now, i.id, None, len(res1.queue), "IN -> 1"])
    with res1.request() as req:
        yield req
        timecount = randint(5, 8)
        yield env.timeout(timecount)
        log.append([env.now, i.id, timecount, len(res1.queue), "OUT -> 1"])
        i.change(timecount)

# class ResourceOneComponent:
#     def __init__(self) -> None:
#         pass
#
#     def Process(self, i: Item):
#         log.append([env.now, i.id, None, res.count, "IN -> 0"])
#         with res.request() as req:
#             yield req
#             timecount = randint(5, 8)
#             yield env.timeout(timecount)
#             log.append([env.now, i.id, timecount, res.count, "OUT -> 0"])
#             i.change(timecount)
#
# class ResourceTwoComponent:
#     def __init__(self) -> None:
#         pass
#
#     def Process(self, i: Item):
#         log.append([env.now, i.id, None, res1.count, "IN -> 1"])
#         with res1.request() as req:
#             yield req
#             timecount = randint(5, 8)
#             yield env.timeout(timecount)
#             log.append([env.now, i.id, timecount, res1.count, "OUT -> 1"])
#             i.change(timecount)
#

def runme(i):
    yield env.process(pro(i))
    # yield env.process(pro1(i))
    print(f'{env.now} ---> runme ')

def mainproc():
    for i in range(20):
        t = Item(i)
        env.process(runme(t))
        yield env.timeout(2)

env.process(mainproc())

env.run()
pprint(log)


