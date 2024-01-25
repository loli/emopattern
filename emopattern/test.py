# SuperFastPython.com
# example of adding a done callback function to a task
import time
import asyncio


# custom done callback function
def callback(task):
    # report a message
    print("Task is done")


# define a coroutine for a task
async def task_coroutine():
    # report a message
    print("executing the task")
    # block for a moment
    await asyncio.sleep(1)


# custom coroutine
async def main():
    # report a message
    print("main coroutine started")
    # create and schedule the task
    task = asyncio.create_task(task_coroutine())
    # add a done callback function
    task.add_done_callback(callback)
    # wait for the task to complete
    for i in range(20):
        print("main sleeps 1 sec")
        time.sleep(1)
    # report a final message
    print("main coroutine done")


# start the asyncio program
asyncio.run(main())
