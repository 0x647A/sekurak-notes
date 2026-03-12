# Markdown to ANSI Terminal Converter

This Python script converts simple Markdown-style formatted text to ANSI-colored text for styled terminal output. It's especially useful for previewing Markdown (headers, bold, italics, lists, inline code, and code blocks) with colors and formatting directly in a Linux/macOS terminal or any ANSI-compatible environment.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Supported Markdown Syntax](#supported-markdown-syntax)
- [How It Works](#how-it-works)
- [Notes](#notes)

## Description

The script parses basic Markdown text and converts it to ANSI escape sequences to apply colors and styles such as:

- Colored headers (h1, h2, h3)
- Bold and italic
- Colored list bullets
- Inline code segments
- Code blocks with themed background

The result is printed to the terminal and saved to a file.

## Features

- Converts:
  - Headings (`#`, `##`, `###`)
  - Bold (`**text**`)
  - Italics (`*text*`)
  - Inline code (`` `code` ``)
  - Unordered lists (`- item`)
  - Fenced code blocks (triple backtick fences)
- Assigns different ANSI colors/styles for each Markdown element
- Outputs colored content to the terminal and saves to a text file for review

## Requirements

- Python 3.6 or newer
- No third-party modules required (`re` is from the standard library)
- Terminal or console that supports ANSI escape codes

## Usage

1. Save the script as `markdown_to_ansi_colors.py`.
2. Place your Markdown-formatted text in a variable or load from a file (see `sample_md` in the script).
3. Run the script:

```bash
python3 markdown_to_ansi_colors.py
```

- The script will print the ANSI-formatted text to the console.
- It also saves the output to `output_ansi.txt`.

## Supported Markdown Syntax

| Markdown Example         | Result         |
|-------------------------|----------------|
| `# Heading 1`           | Red bold       |
| `## Heading 2`          | Green bold     |
| `### Heading 3`         | Blue bold      |
| `**bold**`              | Bold           |
| `*italic*`              | Italic         |
| `` `inline code` ``     | Orange code color |
| Triple backtick fence       | Gray background (code block) |
| `- List item`           | Yellow bullet  |

Currently only simple, single-line constructs are supported (no nested lists, advanced links, or images).

## How It Works

- Splits the input into lines.
- Tracks whether inside a fenced code block.
- Applies corresponding ANSI color/style escape codes to:
  - Headings by line prefix (`startswith`)
  - Bold, italic, and inline code by regex
  - Unordered lists by regex
  - Code blocks by replacing text background
- Assembles the formatted string for display and saves to `output_ansi.txt`.

## Notes

- Make sure your terminal supports ANSI coloring for proper display.
- The converter is basic and not a full Markdown parser—it's ideal for prototyping and learning.
- You can extend the regex patterns for more Markdown features as desired.
