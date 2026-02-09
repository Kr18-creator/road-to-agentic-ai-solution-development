# Concurrency

- Concurrency, or parallelism, is doing multiple computation tasks at a time.
- Computing workloads are often I/O bound
    - Waiting on disk or network.
    - Take advantage of this and work on something else.
- Modern computers have multiple processors.
- Python provides several standard libraries for concurrency
    - `threading`: Mechanism for handling I/O bound computing.
    - `asyncio`: Mechanism for handling I/O bound computing.
    - `multiprocessing`: How to use multi processing. Compute bound.
- Global Interpreter Lock (GIL)
