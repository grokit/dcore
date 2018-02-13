
import os

import dcore.data as data

dbFile = os.path.join(data.dcoreData(), 'work_tracking_db.json')
htmlFile = os.path.join(data.dcoreTempData(), 'work_tracking.html')
dataFile = os.path.join(data.dcoreTempData(), 'data.js')
mainDir = os.path.abspath(os.path.dirname(__file__))
utFolder = os.path.abspath('./unit_tests_inout')

