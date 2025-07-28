# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a generalized Korean lottery ticket generator that can be used for any organization. The system processes email lists and generates printable HTML lottery tickets with unique sequential numbers and customizable organization names.

## Core Commands

```bash
# Generate tickets with single command
python3 lottery_generator.py emails.csv "조직명"

# With custom output filename
python3 lottery_generator.py emails.csv "조직명" -o my_tickets.html

# Example usage
python3 lottery_generator.py emails.csv "2024 카카오 게임동호회"
python3 lottery_generator.py test_emails.csv "테스트 이벤트" -o test_tickets.html

# Help
python3 lottery_generator.py --help
```

## Architecture

The main script `lottery_generator.py` handles the entire workflow in a single command:
- Reads email CSV file directly
- Accepts organization name as command line parameter
- Generates tickets HTML with proper A4 layout
- No intermediate files needed

### Data Flow
```
emails.csv + organization_name → lottery_generator.py → tickets.html
```

### Key Components

- **Number Assignment**: Uses Python's `random.shuffle()` to randomly assign sequential numbers to emails
- **Ticket Layout**: CSS Grid layout with 2 columns × 5 rows per A4 page (10 tickets per page)
- **Ticket Design**: Split design with dotted line - left side (보관용/keep), right side (추첨용/draw)
- **Page Distribution**: Smart algorithm distributes tickets across pages to minimize empty spaces

### File Structure
- `lottery_generator.py`: Main script for generating lottery tickets
- `emails.csv`: Input file with one email per line
- `tickets.html`: Final printable HTML output with custom organization name
- Generated tickets are 320px × 90px, optimized for A4 printing

### Important Implementation Details

- Organization name provided as command line argument
- Email CSV file path as first argument
- Optional `-o` flag for custom output filename
- Built-in error handling and user-friendly messages
- Progress indicators during execution
- Direct email-to-HTML generation (no intermediate files)
- Tickets are sorted by number in ascending order in the final output
- CSS uses `@page` rules for proper A4 printing with 2cm margins
- Empty tickets are hidden using `visibility: hidden` to maintain grid layout
- Print styles ensure tickets don't break across pages (`page-break-inside: avoid`)
