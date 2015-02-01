import sys
import os

sys.path.append(os.path.abspath('..'))

for p in sys.path:
	print(p)

import system_setup.create_python_scripts_shortcuts
system_setup.create_python_scripts_shortcuts.do()
