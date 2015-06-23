
import os
import re

def getCreatedAt(f):
    """
    Return in simple YYYY-MM-DD format.
    """
    
    m = re.search(

    date = datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')
    return date.strftime("%Y-%m-%d") #?? this is localtime or UTC?
