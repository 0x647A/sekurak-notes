# Concurrent Printing Examples in Python

This directory contains three Python scripts that each print the words `"ALA"`, `"MA"`, and `"KOTA"` at fixed intervals, using three different concurrency approaches:

- **Multiprocessing** — multiple OS processes
- **Threading** — multiple threads within one process
- **Manual event loop** — single-threaded, time-based scheduling

## Table of Contents

- [Overview](#overview)
- [Scripts](#scripts)
  - [1. Multiprocessing](#1-multiprocessing)
  - [2. Manual Event Loop](#2-manual-event-loop)
  - [3. Threading](#3-threading)
- [Usage](#usage)
- [Comparison](#comparison)
- [Notes](#notes)

## Overview

All three scripts produce the same observable output: three words printed repeatedly at different intervals.

| Word | Interval (seconds) |
|------|--------------------|
| ALA  | 0.1                |
| MA   | 0.35               |
| KOTA | 0.66               |

Each script demonstrates a different way to achieve this concurrent timing.

## Scripts

### 1. Multiprocessing

- Starts three separate OS processes, each running an infinite loop printing one word and sleeping for its interval.
- Uses Python's `multiprocessing` module with daemon processes that terminate automatically when the main process exits.
- The main process sleeps indefinitely to keep the child processes alive.

### 2. Manual Event Loop

- Runs in a single thread and process.
- A loop continuously checks the current system time against three independently scheduled "next print" timestamps.
- Prints a word when its scheduled time arrives, then advances the timestamp by the word's interval.
- Sleeps briefly (`LOOP_SLEEP = 0.01s`) each iteration to avoid busy-waiting.
- Demonstrates time-based scheduling without threads or processes.

### 3. Threading

- Starts three daemon threads, each running an infinite loop printing one word with its own sleep interval.
- The main thread sleeps indefinitely to keep the daemon threads alive.

## Usage

Requires Python 3.10+. No external dependencies — uses the standard library only.

Run each script separately:

```bash
python3 multiprocessing_test.py  # multiprocessing
python3 nothing_test.py          # manual event loop
python3 threading_test.py        # threading
```

Press `Ctrl+C` to stop.

## Comparison

| Feature             | Multiprocessing            | Manual Event Loop              | Threading                    |
|---------------------|----------------------------|--------------------------------|------------------------------|
| Concurrency model   | Separate OS processes      | Single-threaded, time-scheduled | Multiple threads             |
| GIL impact          | None (isolated processes)  | N/A                            | Shared; released during I/O and `sleep()` |
| Resource usage      | Highest                    | Lowest                         | Moderate                     |
| Timing precision    | OS process scheduler       | Bounded by `LOOP_SLEEP`        | OS thread scheduler          |
| Output interleaving | Possible                   | None (sequential per loop)     | Possible                     |
| Complexity          | Moderate                   | Simple                         | Simple                       |

## Notes

- Output from multiprocessing and threading variants may appear interleaved because writes to stdout are not synchronized across processes or threads.
- The manual event loop produces sequential output within each iteration, so interleaving is not possible — but timing can drift slightly if the loop body is slow.
- Daemon processes and threads terminate when the main process exits — no graceful cleanup is implemented, which is acceptable here but should be addressed in long-running production code.
- For production use, consider `threading.Event` or `asyncio` for cooperative cancellation and graceful shutdown.
