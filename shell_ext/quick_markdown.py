
import markdown
import sys
import glob

"""
#TODO

"""

_meta_shell_command = 'markdown'

autor_pre = """
<html>
<head>
<script type="text/JavaScript">

function timedRefresh(timeoutPeriod) 
{
  setTimeout("location.reload(true);", timeoutPeriod);
}

</script>
</head>
<body onload="JavaScript:timedRefresh(1000);">
<b>Warning: enabled Markdown writing mode.</b>
"""

autor_post = """
</body>
</html>
"""

html_pre = """
<html>
<head>

<style media="screen" type="text/css">
__css__
</style>
</head>
"""

html_post = """
</body>
</html>
"""

css = """
body 
{
    margin: 20px 0;
    margin-left: 100px;
    margin-right: 200px;
    background: #fdfdf6;
}

body, th, td, input, textarea 
{
    font-family: Helvetica;
    font-size: 13px;
    color: #080808;
}

h1, h2, h3 
{
    margin-top: 0.5em;
    font-family: Helvetica;
    color: #416b45;
}

h1 
{
    font-size: 2.3em;
}

h2 
{
    font-size: 1.6em;
}

h3 
{
    font-size: 1.1em;
}

p 
{
    margin-top: 0.5em;
    line-height: 1.5em;
    font-size: 1.1em;
}

a 
{
}
"""

html_pre = html_pre.replace('__css__', css)

javanowing = False
html_pre_post = True

def do():
    
    files = []
    if len(sys.argv) == 2:
        files += sys.argv[1]
    
    if len(files) == 0:
        files += glob.glob('*.markdown')
        files += glob.glob('*.md')
        
    print("Using files: %s" % files)
    
    for file in files:
        fh = open(file, 'r')
        mdstr = fh.read()
        fh.close()

        html = markdown.markdown(mdstr, ['fenced_code', 'codehilite'])

        filename = file + '.html'
        filename = filename.replace('.md', '')
        fh = open(filename, 'w')
        if javanowing:
            fh.write(autor_pre + html + autor_post)
        elif html_pre_post:
            fh.write(html_pre + html + html_post)
        else:
            fh.write(html)
        fh.close()

if __name__ == "__main__":
    do()
    