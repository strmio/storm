# Benchmark setup
import time
from storm.core.context import AppContext
from storm.core.settings import get_settings

from storm.core.router.router import Router
from rich import print

AppContext.set_settings(get_settings())


def handler(request):
    """
    A dummy request handler that simulates processing a request.
    """
    return {"status": "success", "data": request}


def benchmark_router(router_class, n_static=5000, n_dynamic=5000, n_requests=100000):
    router = router_class()

    # Add static routes
    for i in range(n_static):
        router.add_route("GET", f"/static/path/{i}", handler)

    # Add dynamic routes
    for i in range(n_dynamic):
        router.add_route("GET", f"/dynamic/path/:id{i}", handler)

    # Resolve a bunch of routes
    start_time = time.time()
    for i in range(n_requests):
        if i % 2 == 0:
            router.resolve("GET", f"/static/path/{i % n_static}")
        else:
            router.resolve("GET", f"/dynamic/path/value{i % n_dynamic}")
    end_time = time.time()

    return end_time - start_time


if __name__ == "__main__":
    import threading
    from rich.console import Console
    from rich.table import Table

    console = Console()

    def stress_test_concurrent(router_class, n_threads=50, n_requests_per_thread=2000):
        router = router_class()
        for i in range(5000):
            router.add_route("GET", f"/static/path/{i}", handler)
            router.add_route("GET", f"/dynamic/path/:id{i}", handler)

        def worker():
            for i in range(n_requests_per_thread):
                if i % 2 == 0:
                    router.resolve("GET", f"/static/path/{i % 5000}")
                else:
                    router.resolve("GET", f"/dynamic/path/value{i % 5000}")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        start_time = time.time()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        end_time = time.time()
        return end_time - start_time

    # You would replace OptimizedRouter with your original Router for comparison

    print(
        f"Running benchmark with {5000} static routes, {5000} dynamic routes, {100000} requests."
    )
    print("Benchmarking Optimized Router...")
    optimized_time = benchmark_router(Router)
    print(f"Optimized Router Time: {optimized_time * 1000:.2f} ms")

    # If you also want to benchmark the original version, you can add:
    # print("Benchmarking Original Router...")
    # original_time = benchmark_router(OriginalRouter)
    # print(f"Original Router Time: {original_time:.4f} seconds")

    # And compare:
    # print(f"Speedup: {original_time / optimized_time:.2f}x faster!")

    print(
        f"Running concurrent stress test with {50} threads and {2000} requests per thread."
    )
    print("Running concurrent stress test...")
    concurrent_time = stress_test_concurrent(Router)
    print(f"Concurrent Stress Test Time: {concurrent_time * 1000:.2f} ms")

    table = Table(title="Router Benchmark Summary")

    table.add_column("Test", style="cyan", no_wrap=True)
    table.add_column("Requests", justify="right", style="magenta")
    table.add_column("Time (ms)", justify="right", style="green")

    table.add_row("Sequential Benchmark", "100,000", f"{optimized_time * 1000:.2f}")
    table.add_row("Concurrent Stress Test", "100,000", f"{concurrent_time * 1000:.2f}")

    console.print(table)
