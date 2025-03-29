""" script for comparing serial and async execution"""

import time
import asyncio
import tracemalloc
from logger import setup_logger
import serial as serial_main
from main import main as async_main
import datetime 
import os 
from logger import benchmark_logger
import platform
import psutil
def benchmark_serial():
    benchmark_logger.info(
    f"Processor Details:\n"
    f"  Processor: {platform.processor()}\n"
    f"  Cores: {psutil.cpu_count(logical=False)}\n"
    f"  Threads: {psutil.cpu_count(logical=True)}\n"
    f"  CPU Frequency (MHz): {psutil.cpu_freq().max if psutil.cpu_freq() else 'Unknown'}"
    )
    net_stats = psutil.net_io_counters()
    benchmark_logger.info(
        f"Network Stats:\n"
        f"  Bytes Sent: {net_stats.bytes_sent}\n"
        f"  Bytes Received: {net_stats.bytes_recv}\n"
        f"  Packets Sent: {net_stats.packets_sent}\n"
        f"  Packets Received: {net_stats.packets_recv}\n"
        f"  Dropped Packets In: {net_stats.dropin}\n"
        f"  Dropped Packets Out: {net_stats.dropout}\n"
        f"  Errors In: {net_stats.errin}\n"
        f"  Errors Out: {net_stats.errout}"
    )

    benchmark_logger.info("Starting serial execution benchmarking...")
    tracemalloc.start()
    start_time = time.time()
    serial_main.main()
    end_time = time.time()
    memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    execution_time = end_time - start_time
    benchmark_logger.info(f"Serial Execution Time: {execution_time:.2f} seconds")
    benchmark_logger.info(f"Peak Memory Usage: {memory_usage[1] / 1024:.2f} KB")
    
    return execution_time, memory_usage[1] / 1024

async def benchmark_async():
    benchmark_logger.info("Starting async execution benchmarking...")
    tracemalloc.start()
    start_time = time.time()
    await async_main()
    end_time = time.time()
    memory_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    execution_time = end_time - start_time
    benchmark_logger.info(f"Async Execution Time: {execution_time:.2f} seconds")
    benchmark_logger.info(f"Peak Memory Usage: {memory_usage[1] / 1024:.2f} KB")
    
    return execution_time, memory_usage[1] / 1024

def main():
    serial_time, serial_memory = benchmark_serial()
    async_time, async_memory = asyncio.run(benchmark_async())
    
    benchmark_logger.info("Benchmark Results:")
    benchmark_logger.info(f"Serial Execution: {serial_time:.2f} sec, {serial_memory:.2f} KB memory")
    benchmark_logger.info(f"Async Execution: {async_time:.2f} sec, {async_memory:.2f} KB memory")
    
    improvement = (serial_time - async_time) / serial_time * 100
    benchmark_logger.info(f"Performance Improvement: {improvement:.2f}%")
    
if __name__ == "__main__":
    main()
 