
import datetime

# Seattle FTW
timeZone = datetime.timezone(datetime.timedelta(hours=-7))

def dateNow():
    return datetime.datetime.now(timeZone)

def dateNowStr():
    return dateNow().isoformat()

def dateStrToDateTime(d):
    # '2015-10-03T16:15:30.200216+00:00' does not match format 
    # '%Y-%m-%dT%H:%M:%S.%f+%z'
    # ^^ there is an extra ':' in the timeZone
    assert d[-3] == ':'
    d = d[0:-3] + d[-2:]

    # http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand
    dt = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt
    #return dt.replace(tzinfo=datetime.timezone.utc).astimezone(timeZone=tz)

def dateTimeToStr(dt):
    #dt = dt.replace(tzinfo=datetime.timezone.utc).astimezone(timeZone=tz)
    dt = dt.isoformat()
    return dt
