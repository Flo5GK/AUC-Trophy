# Initialize the screen
import curses

screen = curses.initscr()

# Check if screen was re-sized (True or False)
while True:
    resize = curses.is_term_resized(y, x)

    # Action in loop if resize is True:
    if resize is True:
        y, x = screen.getmaxyx()
        screen.clear()
        curses.resizeterm(y, x)
        screen.refresh()