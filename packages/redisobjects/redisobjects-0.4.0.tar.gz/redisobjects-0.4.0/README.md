Redisobjects
============

Simple wrapper for [aioredis](https://github.com/aio-libs/aioredis) to provide asynchronous functionality with a clean object-oriented interface for Redis in Python 3.6+.

Installation
------------

```shell
pip install redisobjects
```

Examples
--------

Example showing how to use atoms (defined as single key-value pairs):

```python
import redisobjects
import asyncio

async def main(loop):
    redis = await redisobjects.connect('redis://localhost', loop=loop)
    atom = redis.atom('example.atom')
    print(await atom.get())
    await atom.set('bla')
    print(await atom.get())
    await atom.remove()
    print(await atom.get())
    redis.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```

Example that shows how to use a list:

```python
import redisobjects
import asyncio

async def main(loop):
    redis = await redisobjects.connect('redis://localhost', loop=loop)
    example_list = redis.list('example.list')
    print(await example_list.list())
    await example_list.push_right('b')
    await example_list.push_right('c')
    print(await example_list.list())
    await example_list.push_left('a')
    print(await example_list.list())
    await example_list.pop_left()
    await example_list.pop_left()
    print(await example_list.list())
    await example_list.pop_left()
    print(await example_list.list())
    redis.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```

Example that shows how to use a dict/map:

```python
import redisobjects
import asyncio

async def main(loop):
    redis = await redisobjects.connect('redis://localhost', loop=loop)
    d = redis.dict('example.dict')
    print(dict(await d.items()))
    await d.set('a', '1')
    print(dict(await d.items()))
    await d.set('b', '2')
    print(dict(await d.items()))
    await d.set('c', '3')
    print(dict(await d.items()))
    await d.remove('a', 'b')
    print(dict(await d.items()))
    await d.remove('c')
    print(dict(await d.items()))
    redis.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
```
