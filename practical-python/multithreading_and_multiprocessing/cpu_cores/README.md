# macOS CPU Information Script

This Python script retrieves basic CPU information on macOS systems by running `sysctl` commands via the `subprocess` module. It fetches and displays:

- CPU model name
- Number of physical cores
- Number of logical cores (threads)

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
- [Function Descriptions](#function-descriptions)
- [Sample Output](#sample-output)
- [Notes](#notes)

## Description

The script queries CPU details on macOS using three `sysctl` keys:

- `machdep.cpu.brand_string` — human-readable CPU model name (Intel only; Apple Silicon falls back gracefully)
- `hw.physicalcpu` — number of physical CPU cores
- `hw.logicalcpu` — number of logical CPU cores

It uses the `subprocess` module to run the commands and captures their output for display.

## Requirements

- Python 3.10+
- macOS (the `sysctl` keys used are macOS-specific and unavailable on Linux or Windows)

## Usage

```bash
python3 cpu_physical_and_logical_cores.py
```

## Function Descriptions

- `get_cpu_model() -> str`
  Returns the CPU model name. On Apple Silicon, returns a fallback string since `machdep.cpu.brand_string` is an Intel-only sysctl key.

- `get_physical_cores() -> int`
  Returns the number of physical CPU cores.

- `get_logical_cores() -> int`
  Returns the number of logical CPU cores.

## Sample Output

On Intel Mac:
```
CPU Model: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
Physical Cores: 6
Logical Cores (Threads): 12
```

On Apple Silicon (M-series):
```
CPU Model: Apple Silicon (model unavailable via sysctl)
Physical Cores: 10
Logical Cores (Threads): 10
```

## Notes

- This script is macOS-only. On Linux, use `/proc/cpuinfo` or the `psutil` library. On Windows, use `wmic` or `psutil`.
- `machdep.cpu.brand_string` is an x86 (Intel) sysctl key and does not exist on Apple Silicon. The script handles this gracefully.
- `hw.physicalcpu` and `hw.logicalcpu` work correctly on both Intel and Apple Silicon Macs.
