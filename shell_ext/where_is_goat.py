"""
"""

import argparse
import random
import math

_meta_shell_command = 'where_is_goat'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spiral', action='store_true', default=False)
    return parser.parse_args()


if __name__ == '__main__':

    args = getArgs()

    if args.spiral:
        emoji = [':goat:', ':turtle:', ':last_quarter_moon_with_face:']
        symbol = '??'
        ln = [[symbol for i in range(16)] for i in range(16)]

        y0 = int(len(ln) / 2)
        x0 = int(len(ln[0]) / 2)
        pos = [y0, x0]
        npr = 100
        spd = 6

        for i in range(npr):
            pos[1] = int(y0 + math.sin(spd * math.pi * (i / npr)) * x0 *
                         (i / npr))
            pos[0] = int(x0 + math.cos(spd * math.pi * (i / npr)) * y0 *
                         (i / npr))
            ln[pos[0]][pos[1]] = emoji[i % len(emoji)]

        for line in ln:
            print("".join(line))

    else:
        emoji = [':turtle:', ':goat']
        ln = '???????????????????'
        dr = 1
        step = 6
        pos = int(random.random() * len(ln))
        if random.random() < 0.5: dr *= -1

        for i in range(100):
            pos = min(len(ln) - 1, pos)
            pos = max(0, pos)
            line = ln[0:pos] + emoji[i % len(emoji)] + ln[pos:]
            print(line)
            cstep = int(step * 0.7 + step * 1.2 * random.random())
            pos += cstep * dr
            if pos < 0 or pos >= len(ln):
                dr *= -1
                pos += int(1.5 * cstep * dr)
