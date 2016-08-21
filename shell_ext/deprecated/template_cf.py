import sys

_meta_shell_command = 'template_cf'

template = """\"\"\"
\"\"\"
"""

if __name__ == '__main__':
    name = 'code.py'

    if len(sys.argv) > 1:
        name = sys.argv[1]

    open(name, 'w').write(template)
