
import search

_meta_shell_command = 'time_fix_'

if __name__ == '__main__':

    files = search.getAllFiles()

    for f in files:
        with open(f, 'r') as fh:
            lines = fh.readlines()

        mod = False
        lo = []
        for l in lines:
            if 'time::' in l:
                mod = True
                l = l.replace(' ', '_')
            lo.append(l)
        lines = "".join(lo)

        if mod:
            with open(f, 'w') as fh:
                fh.write(lines)

