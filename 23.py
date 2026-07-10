#!/usr/bin/env python3
import curses
import random
import time

# Game constants
ROWS, COLS = 20, 60
GRAVITY = 0.2
FLAP_STRENGTH = -4.5
PIPE_WIDTH = 4
GAP_HEIGHT = 5
PIPE_SPEED = 1.2
FRAME_DELAY = 0.03  # seconds

def draw_game(stdscr, bird_y, pipe_x, gap_top, score, game_over):
    """Render the entire game state to the terminal."""
    stdscr.clear()

    # Draw ground
    for c in range(COLS):
        stdscr.addch(ROWS - 1, c, '_')

    # Draw ceiling (visual only)
    for c in range(COLS):
        stdscr.addch(0, c, '-')

    # Draw bird (flap animation based on velocity)
    bird_char = '@' if not game_over else 'X'
    stdscr.addch(int(bird_y), 5, bird_char)

    # Draw pipes
    for i in range(PIPE_WIDTH):
        x = int(pipe_x) + i
        if x >= COLS or x < 0:
            continue
        # Top pipe (from ceiling to gap start)
        for y in range(1, gap_top):
            stdscr.addch(y, x, '#')
        # Bottom pipe (from gap end to ground)
        for y in range(gap_top + GAP_HEIGHT, ROWS - 1):
            stdscr.addch(y, x, '#')

    # Draw score
    stdscr.addstr(2, COLS // 2 - 3, f"🏆 {score}")

    # Game over overlay
    if game_over:
        stdscr.addstr(ROWS // 2 - 2, COLS // 2 - 6, " GAME OVER ")
        stdscr.addstr(ROWS // 2, COLS // 2 - 10, "Press 'r' to retry")
        stdscr.addstr(ROWS // 2 + 1, COLS // 2 - 10, "Press 'q' to quit")

    stdscr.refresh()

def main(stdscr):
    # Terminal setup
    curses.curs_set(0)      # Hide cursor
    stdscr.nodelay(1)       # Non-blocking input
    stdscr.timeout(50)      # Input timeout (ms)

    # Game state
    bird_y = ROWS // 2
    bird_vel = 0.0
    pipe_x = COLS - 1
    gap_top = random.randint(2, ROWS - GAP_HEIGHT - 3)
    score = 0
    game_over = False
    scored = False  # Prevents multiple score increments per pipe

    while True:
        # --- 1. Input Handling ---
        key = stdscr.getch()
        if key == ord('q'):
            break
        if not game_over and key == ord(' '):
            bird_vel = FLAP_STRENGTH
        if game_over and key == ord('r'):
            # Reset state
            bird_y = ROWS // 2
            bird_vel = 0.0
            pipe_x = COLS - 1
            gap_top = random.randint(2, ROWS - GAP_HEIGHT - 3)
            score = 0
            game_over = False
            scored = False
            continue

        # --- 2. Physics Update (only if playing) ---
        if not game_over:
            # Bird physics
            bird_vel += GRAVITY
            bird_y += bird_vel

            # Pipe movement
            pipe_x -= PIPE_SPEED

            # Score when pipe passes bird's x position
            if not scored and pipe_x + PIPE_WIDTH < 5:
                score += 1
                scored = True

            # Spawn new pipe
            if pipe_x < -PIPE_WIDTH:
                pipe_x = COLS - 1
                gap_top = random.randint(2, ROWS - GAP_HEIGHT - 3)
                scored = False

            # --- 3. Collision Detection ---
            # Ground / Ceiling hit
            if bird_y <= 0 or bird_y >= ROWS - 2:
                game_over = True

            # Pipe hit
            bird_x = 5
            # Check if bird's x overlaps with any pipe column
            if pipe_x <= bird_x <= pipe_x + PIPE_WIDTH - 1:
                if bird_y <= gap_top or bird_y >= gap_top + GAP_HEIGHT:
                    game_over = True

        # --- 4. Render ---
        draw_game(stdscr, bird_y, pipe_x, gap_top, score, game_over)
        time.sleep(FRAME_DELAY)

curses.wrapper(main)