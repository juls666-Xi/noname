#!/usr/bin/env python3
import curses
import random
import time

def main(stdscr):
    # Hide cursor, make getch non‑blocking
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(0)

    # Init colors (1 = bright green, 2 = normal green)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    sh, sw = stdscr.getmaxyx()
    if sh < 5 or sw < 10:
        print("Terminal too small – make it at least 10x5")
        return

    # Each column: [head_row, speed, streak_length]
    columns = []
    for _ in range(sw):
        columns.append([
            random.randint(0, sh),
            random.randint(1, 3),
            random.randint(5, 15)
        ])

    while True:
        stdscr.erase()
        for col in range(sw):
            head, speed, length = columns[col]

            # Draw the streak from head downwards
            for offset in range(length):
                row = head - offset
                if row < 0 or row >= sh:
                    continue
                char = chr(random.randint(33, 126))  # printable ASCII

                # Head = bright + bold, rest = normal green
                if offset == 0:
                    stdscr.addch(row, col, char,
                                 curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addch(row, col, char, curses.color_pair(2))

            # Move the drop down
            columns[col][0] += speed

            # Reset if fully off‑screen (or randomly, for variety)
            if columns[col][0] - length > sh or random.random() < 0.005:
                columns[col][0] = 0
                columns[col][1] = random.randint(1, 3)
                columns[col][2] = random.randint(5, 15)

        stdscr.refresh()
        time.sleep(0.035)

if __name__ == "__main__":
    curses.wrapper(main)