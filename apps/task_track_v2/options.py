
import os

import dcore.data as data

dbFile = os.path.join(data.dcoreRoot(), 'work_tracking_db.json')
htmlFile = os.path.join(data.dcoreRoot(), 'work_tracking.html')
mainDir = os.path.abspath(os.path.dirname(__file__))
utFolder = os.path.abspath('./unit_tests_inout')

