"""
Turn-off (or on) procrastination websites.
"""

import argparse

from dcore import env_setup

_meta_shell_command = 'work_mode'

WEBSITES = [
    'twitter.com', 'reddit.com', 'youtube.com', 'news.ycombinator.com',
    'facebook.com'
]
HOST_FILE = '/etc/hosts'


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--on', action="store_true")
    parser.add_argument('--off', action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = getArgs()
    assert args.on or args.off

    content = "# Nothing disabled. Don't binge too much! Moderation in all things."
    if args.on:
        content = []
        for website in WEBSITES:
            content.append('127.0.0.1 %s' % website)
            content.append('127.0.0.1 www.%s' % website)
        content = "\n".join(content)

    mark_begin = '# ' + __file__ + " BEGIN"
    mark_end = '# ' + __file__ + " END"
    env_setup.updateFileContentBetweenMarks(HOST_FILE, mark_begin, mark_end,
                                            content, False)
    print('Done. Your system may require a reboot before change take effect.')
