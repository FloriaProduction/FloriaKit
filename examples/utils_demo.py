"""Демонстрация утилит из FloriaKit.utils."""

import asyncio
import time

from FloriaKit import hints, utils
from FloriaKit.utils import vector, matrix, quaternion
from FloriaKit.utils.avg import Avg
from FloriaKit.utils.flag import Flag
from FloriaKit.utils.interpolation_field import InterpolationField
from FloriaKit.utils.calculated_fields import CalculatedFields
from FloriaKit.utils.calculated_value import CalculatedValue, gcv
from FloriaKit.utils.stopwatch import Stopwatch, stopwatch

# -------------------- Avg --------------------

avg = Avg()
avg.add(10).add(20).add(30)
print(f"Avg: {avg.value} (count={avg.count}, total={avg.total})")


# -------------------- coalapse --------------------
first_none = None
second_none = None
value = 42
result = utils.coalapse(first_none, second_none, value, default="default")
print(f"coalapse: {result}")  # 42


# Lazy version – вычисляется только первый не-None
lazy_result = utils.coalapse_lazy(None, lambda: 100, default=0)
print(f"coalapse_lazy: {lazy_result}")  # 100


# -------------------- invoke (синхр/асинхр) --------------------
async def async_greet(name: str) -> str:
    await asyncio.sleep(0.01)
    return f"Hello, {name}"


def sync_greet(name: str) -> str:
    return f"Hi, {name}"


async def demo_invoke():
    print(await utils.invoke(sync_greet, "World"))  # Hi, World
    print(await utils.invoke(async_greet, "Async"))  # Hello, Async


# -------------------- partition --------------------
items: list[int | None] = [1, None, 3, None, 5]

trues, falses = utils.partition(lambda x: x is not None, items)

# Или

trues, falses = utils.partition(None, items)

print(f"Partition: trues={trues}, falses={falses}")


# -------------------- ensure_iterable --------------------
print(utils.ensure_iterable("hello"))  # ['hello']
print(utils.ensure_iterable(100))  # [100]
print(utils.ensure_iterable([1, 2, 3]))  # [1, 2, 3]


# -------------------- context.empty --------------------
with utils.context.empty("temp value") as val:
    print(f"Context empty: {val}")  # temp value


async def demo_empty_async():
    async with utils.context.empty_async("async temp") as val:
        print(f"Empty async: {val}")


# -------------------- Flag --------------------
flag = Flag()
print(f"Flag initial: {bool(flag)}")  # False
with flag:
    print(f"Inside context: {bool(flag)}")  # True
print(f"After context: {bool(flag)}")  # False


# -------------------- InterpolationField --------------------
def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


interp = InterpolationField(lerp, delay=0.5, default=0.0)
interp.set_value(100.0)
print(f"Progress immediately: {interp.progress:.2f}")  # 0.0
time.sleep(0.25)
print(f"Progress after 0.25s: {interp.progress:.2f}")  # ~0.5
print(f"Value after 0.25s: {interp.get_value():.1f}")  # ~50.0
time.sleep(0.3)
print(f"Final value: {interp.get_value()}")  # 100.0


# -------------------- stopwatch & Stopwatch --------------------
@stopwatch
def measured_function():
    time.sleep(0.05)


measured_function()

measured_function.__stopwatch__.last  # получение время выполнения

# Или

sw = Stopwatch(max_samples=5)
with sw:
    time.sleep(0.05)
print(f"Last: {sw.last:.4f}s, Avg: {sw.avg:.4f}s")


# -------------------- vector utilities --------------------
v1: hints.vec2 = (1, 2)
v2: hints.vec2 = (4, 6)
print("Lerp:", vector.lerp(v1, v2, 0.5))  # (2.5, 4.0)
print("Sum:", vector.sum(v1, v2, 10))  # (15, 18)
print("Sub:", vector.sub(v1, v2))  # (-3, -4)
print("Mul:", vector.mul(v1, 3))  # (3, 6)
print("Div:", vector.div(v1, 2))  # (0.5, 1.0)
print("Distance:", vector.distance(v1, v2))  # 5.0
print("Round:", vector.round_((1.2, 2.7)))  # (1, 3)


# -------------------- quaternion utilities --------------------
q_identity: hints.quat = (0, 0, 0, 1)
q_look = quaternion.look_at((0, 0, 0), (1, 0, 0), (0, 1, 0))
print("Look at quat:", q_look)
print("Slerp:", quaternion.slerp(q_identity, q_look, 0.5))


# -------------------- matrix utilities --------------------
model = matrix.model_matrix(position=(0, 0, -5), angle=q_identity, scale=(1, 1, 1))
print("Model matrix (first row):", model[0])
