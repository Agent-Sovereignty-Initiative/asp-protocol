"""
ACN Terminal Display Module
Color-coded output:
  BLUE   = network / protocol layer (public)
  YELLOW = agent-internal / private (never transmitted)
  GREEN  = blockchain writes
  RED    = ZK cryptographic math
  CYAN   = section headers
  WHITE  = neutral info
"""

import time

# ANSI codes
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

BLUE   = "\033[94m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
MAGENTA = "\033[95m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

SLOW = False  # set True for dramatic effect


def _pace(seconds=0.03):
    if SLOW:
        time.sleep(seconds)


def banner(title: str):
    width = 62
    line = "═" * width
    print(f"\n{CYAN}{BOLD}{line}{RESET}")
    pad = (width - len(title)) // 2
    print(f"{CYAN}{BOLD}{' ' * pad}{title}{RESET}")
    print(f"{CYAN}{BOLD}{line}{RESET}\n")
    _pace(0.1)


def step(number: int, title: str):
    print(f"\n{CYAN}{BOLD}┌─ STEP {number}: {title}{RESET}")
    print(f"{CYAN}{'─' * 60}{RESET}")
    _pace(0.05)


def network(msg: str, indent: int = 0):
    prefix = "  " * indent
    print(f"{prefix}{BLUE}🔵 [NETWORK]{RESET}  {msg}")
    _pace(0.02)


def private(msg: str, indent: int = 1):
    prefix = "  " * indent
    print(f"{prefix}{YELLOW}🟡 [PRIVATE — not transmitted]{RESET}  {DIM}{msg}{RESET}")
    _pace(0.02)


def chain(msg: str):
    print(f"{GREEN}🟢 [CHAIN]   {RESET}{msg}")
    _pace(0.02)


def zk_math(msg: str, indent: int = 2):
    prefix = "  " * indent
    print(f"{prefix}{RED}◆ ZK {RESET}{DIM}{msg}{RESET}")
    _pace(0.015)


def info(msg: str, indent: int = 0):
    prefix = "  " * indent
    print(f"{prefix}{WHITE}{msg}{RESET}")
    _pace(0.01)


def success(msg: str):
    print(f"{GREEN}{BOLD}✓ {msg}{RESET}")
    _pace(0.02)


def warn(msg: str):
    print(f"{YELLOW}⚠ {msg}{RESET}")


def divider(char: str = "─", width: int = 60):
    print(f"{GRAY}{char * width}{RESET}")


def report_section(title: str, content: str):
    print(f"\n{MAGENTA}{BOLD}{'═' * 60}{RESET}")
    print(f"{MAGENTA}{BOLD}  {title}{RESET}")
    print(f"{MAGENTA}{'─' * 60}{RESET}")
    for line in content.strip().split("\n"):
        print(f"  {WHITE}{line}{RESET}")
    _pace(0.01)


def block_row(block_num: int, block_type: str, block_hash: str, summary: str):
    hash_short = block_hash[:12] + "..."
    num_str = f"#{block_num:02d}"
    print(f"  {CYAN}{num_str}{RESET}  {GREEN}{block_type:<22}{RESET}  "
          f"{GRAY}{hash_short}{RESET}  {DIM}{summary}{RESET}")
