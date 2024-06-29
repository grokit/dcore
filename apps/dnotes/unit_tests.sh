#!/bin/bash
clear
python3 unit_tests/all.py 

# Note: this is run by external validation script.
# ... be careful renaming, etc.
# It relies on the return value of this script to indicate if there is something wrong,
# and the stdout/err for what's wrong.

