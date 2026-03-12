import re


# ANSI escape codes
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
ITALIC = "\x1b[3m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
BLUE = "\x1b[34m"
YELLOW = "\x1b[33m"
GRAY_BG = "\x1b[48;5;240m"
CODE_COLOR = "\x1b[38;5;208m"


def markdown_to_ansi(md_text: str) -> str:
    """Convert a Markdown-formatted string to ANSI-escaped terminal output."""
    lines = md_text.splitlines()
    in_code_block = False
    output_lines = []

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            output_lines.append(f"{GRAY_BG}{line}{RESET}")
            continue

        if line.startswith("### "):
            line = f"{BLUE}{BOLD}{line[4:]}{RESET}"
        elif line.startswith("## "):
            line = f"{GREEN}{BOLD}{line[3:]}{RESET}"
        elif line.startswith("# "):
            line = f"{RED}{BOLD}{line[2:]}{RESET}"

        line = re.sub(r"^- (.+)", f"{YELLOW}• \\1{RESET}", line)

        line = re.sub(r"`([^`]+)`", f"{CODE_COLOR}`\\1`{RESET}", line)

        # Bold must be processed before italic to avoid * collision:
        # ** contains *, so italic regex would incorrectly match inside bold markers.
        line = re.sub(r"\*\*(.*?)\*\*", f"{BOLD}\\1{RESET}", line)
        line = re.sub(r"\*(.*?)\*", f"{ITALIC}\\1{RESET}", line)

        output_lines.append(line)

    return "\n".join(output_lines)


if __name__ == "__main__":
    sample_md = """\
# Heading 1
## Heading 2
### Heading 3

This is **bold** text and *italic* text. Here's some `inline code`.

- First list item
- Second list item

"""

    ansi_output = markdown_to_ansi(sample_md)

    # Saves output to a file for review in editors that support ANSI codes.
    # Note: this file is created automatically every time the script is run.
    with open("output_ansi.txt", "w", encoding="utf-8") as f:
        f.write(ansi_output)

    print(ansi_output)
