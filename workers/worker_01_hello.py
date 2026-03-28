#!/usr/bin/env python3
"""
Worker Camunda - Module 01 : Hello World
Type de job : log-hello
Installation : pip install pyzeebe
"""
import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel

channel = create_insecure_channel(hostname="localhost", port=26500)
worker = ZeebeWorker(channel)


@worker.task(task_type="log-hello", timeout_ms=10000)
async def handle_hello(job):
    """Handler Service Task log-hello"""
    print("=" * 40)
    print("[Module 01] Hello World depuis Camunda !")
    print(f"Process ID  : {job.process_instance_key}")
    print(f"Job Key     : {job.key}")
    print("=" * 40)
    return {"message": "Hello World", "status": "done"}


async def main():
    print("[Worker 01] Demarrage - en attente de jobs 'log-hello'...")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())
