
ENABLED = True

# https://www.tutorialspoint.com/how-to-output-colored-text-to-a-linux-terminal
COLOR_BEGIN_GREEN = '\033[1;32;48m'
COLOR_BEGIN_BLUE = '\033[;34m'
COLOR_BEGIN_YELLOW = '\033[4;33m'
COLOR_END = '\033[1;37;0m'

def green(ss):
    if ENABLED:
        return "%s%s%s" % (COLOR_BEGIN_GREEN, ss, COLOR_END)
    else:
        return ss

def blue(ss):
    if ENABLED:
        return "%s%s%s" % (COLOR_BEGIN_BLUE, ss, COLOR_END)
    else:
        return ss

def yellow(ss):
    if ENABLED:
        return "%s%s%s" % (COLOR_BEGIN_YELLOW, ss, COLOR_END)
    else:
        return ss
