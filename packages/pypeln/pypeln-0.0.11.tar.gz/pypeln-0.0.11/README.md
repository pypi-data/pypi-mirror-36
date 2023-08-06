# Pypeline

_Pypeline is a python library for easily creating concurrent data pipelines._

* Pypeline was designed to solve simple _medium_ data tasks that require concurrency and parallelism but where using frameworks like Spark or Dask feel exaggerated or unnatural.
* Pypeline exposes an easy to use, familiar, functional API.
* Pypeline enables you to build pipelines using Processes, Threads and asyncio.Tasks via the exact same API.
* Pypeline allows you to have control over the memory and cpu resources used at each stage of your pipeline.

## Instalation

Install Pypeline using pip:
```bash
pip install pypeln
```

## Basic Usage
With Pypeline you can create multi-stage data pipelines using with 3 type of workers:

### Processes
You can create a pipeline based on [multiprocessing.Process](https://docs.python.org/3.4/library/multiprocessing.html#multiprocessing.Process) workers by using the `pr` module:

```python
from pypeln import pr
import time
from random import random

def slow_add1(x):
    time.sleep(random()) # <= some slow computation
    return x + 1

def slow_gt3(x):
    time.sleep(random()) # <= some slow computation
    return x > 3

data = range(10) # [0, 1, 2, ..., 9] 

stage = pr.map(slow_add1, data, workers = 3, maxsize = 4)
stage = pr.filter(slow_gt3, stage, workers = 2)

data = list(stage) # e.g. [5, 6, 9, 4, 8, 10, 7]
```
At each stage the you can specify the numbers of `workers`. The `maxsize` parameter limits the maximum amount of elements that the stage can hold simultaneously.

### Threads
You can create a pipeline based on [threading.Thread](https://docs.python.org/3/library/threading.html#threading.Thread) workers by using the `th` module:
```python
from pypeln import th
import time
from random import random

def slow_add1(x):
    time.sleep(random()) # <= some slow computation
    return x + 1

def slow_gt3(x):
    time.sleep(random()) # <= some slow computation
    return x > 3

data = range(10) # [0, 1, 2, ..., 9] 

stage = th.map(slow_add1, data, workers = 3, maxsize = 4)
stage = th.filter(slow_gt3, stage, workers = 2)

data = list(stage) # e.g. [5, 6, 9, 4, 8, 10, 7]
```
Here we have the exact same situation as in the previous case except that the worker are Threads.

### Tasks
You can create a pipeline based on [asyncio.Task](https://docs.python.org/3.4/library/asyncio-task.html#asyncio.Task) workers by using the `io` module:
```python
from pypeln import io
import asyncio
from random import random

async def slow_add1(x):
    await asyncio.sleep(random()) # <= some slow computation
    return x + 1

async def slow_gt3(x):
    await asyncio.sleep(random()) # <= some slow computation
    return x > 3

data = range(10) # [0, 1, 2, ..., 9] 

stage = io.map(slow_add1, data, workers = 3, maxsize = 4)
stage = io.filter(slow_gt3, stage, workers = 2)

data = list(stage) # e.g. [5, 6, 9, 4, 8, 10, 7]
```
Conceptually similar but everything is running in a single thread and Task workers are created dynamically.

For more information see the [Pypeline Guide](https://cgarciae.gitbook.io/pypeln).

## Pipe Operator
In the spirit of being a true pipeline library, Pypeline also lets you create your pipelines using the pipe `|` operator:

```python
data = (
    range(10)
    | pr.map(slow_add1, workers = 3, maxsize = 4)
    | pr.filter(slow_gt3, workers = 2)
    | list
)
```

## Benchmarks
* [Making an Unlimited Number of Requests with Python aiohttp + pypeln](https://medium.com/@cgarciae/making-an-infinite-number-of-requests-with-python-aiohttp-pypeln-3a552b97dc95)
  * [Code](https://github.com/cgarciae/pypeln/tree/master/benchmarks/100_million_downloads)

## Resources
* [Pypeline Guide](https://cgarciae.gitbook.io/pypeln)
* [Pypeline API Documentation](https://cgarciae.github.io/pypeln/)


## Related Stuff
* [mpipe](https://vmlaker.github.io/mpipe/)
* [Process Pools](https://docs.python.org/3.4/library/multiprocessing.html?highlight=process#module-multiprocessing.pool)
* [Making 100 million requests with Python aiohttp](https://www.artificialworlds.net/blog/2017/06/12/making-100-million-requests-with-python-aiohttp/)
* [Python multiprocessing Queue memory management](https://stackoverflow.com/questions/52286527/python-multiprocessing-queue-memory-management/52286686#52286686)


## Contributors
* [cgarciae](https://github.com/cgarciae)
* [davidnet](https://github.com/davidnet)