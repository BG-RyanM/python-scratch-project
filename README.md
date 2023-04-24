# python-scratch-project

Repo for toy Python programs that demonstrate some specific feature of Python.

## Because I Keep Forgetting

On my laptop, all this lives inside the devbash-1804 container, in `~/PycharmProjects/scratch-project`.

### When `git pull` Freezes

```
$ git fsck && git gc --prune=now
```

Also, try this on HOST (not in container)
```
> sudo iptables -P FORWARD ACCEPT
```

## Stuff That's Here

Script | Purpose
----------------------------|-----------
`arbitrary_members_test.py` | A demonstration of a class whose instances can be dynamically populated with data, easily accessible as member variables.
`arg_parse.py` | How to parse arguments given from command line.
`asyncio_test.py` | Code that demonstrates how to do various things with async functions and tasks.
`asyncio_test2.py` | Demonstrates use of asyncio.Event.
`attr_test.py` | Demonstrates how to use attr library. Also some demonstration of how to make a class cast-able into a Dict.
`attr_test2.py` | Doesn't actually use attr, but shows how to programmatically add data members and functions to an object at runtime. Features use of partial().
`await_test.py` | Test of asyncio gather() combined with a timeout feature. Shows how to run multiple async functions at once, with a timeout to deal with any that don't finish quickly enough.
`base_class_test.py` | Experiments with inheritance, both multiple and single.
`breakable_with_py` | 1) How to create a Python resource. 2) A method for breaking out of "with" blocks.
`callback_test.py` | How to set up and use a callback function.
`class_test.py` | Simple experiments with classes and a factory method that can make classes of an arbitrary type.
`contextlib_test.py` | Code that demonstrates use of contextlib for creating a function that can be used with Python's 'async with`. Also demonstrates a helper function that waits on an asyncio Lock, but with a timeout. 
`coroutine_test.py` | This is the coroutine version of an async function and is Py2-compatible. There is no await in it.

_TODO: finish this list..._





