import subprocess


def _sysctl(key: str) -> str:
    """Run sysctl -n <key> and return the stripped output, or raise RuntimeError on failure."""
    result = subprocess.run(
        ["sysctl", "-n", key],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"sysctl key '{key}' not available on this system.")
    return result.stdout.strip()


def get_cpu_model() -> str:
    """Return the CPU model name.

    Uses machdep.cpu.brand_string (Intel) with a fallback for Apple Silicon.
    """
    try:
        return _sysctl("machdep.cpu.brand_string")
    except RuntimeError:
        # machdep.cpu.brand_string is Intel-only; Apple Silicon exposes no equivalent sysctl key
        return "Apple Silicon (model unavailable via sysctl)"


def get_physical_cores() -> int:
    """Return the number of physical CPU cores."""
    return int(_sysctl("hw.physicalcpu"))


def get_logical_cores() -> int:
    """Return the number of logical CPU cores."""
    return int(_sysctl("hw.logicalcpu"))


if __name__ == "__main__":
    print("CPU Model:", get_cpu_model())
    print("Physical Cores:", get_physical_cores())
    print("Logical Cores (Threads):", get_logical_cores())
