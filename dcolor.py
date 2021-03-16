
ENABLED = True

if ENABLED:
    COLOR_BEGIN_GREEN = '\033[1;32;48m'
    COLOR_END = '\033[1;37;0m'
else:
    COLOR_BEGIN_GREEN = ''
    COLOR_END = ''

def green(ss):
    return "%s%s%s" % (COLOR_BEGIN_GREEN, ss, COLOR_END)
