
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

# From: https://github.com/remy/mit-license/blob/master/themes
css = """
body {
    margin: 20px 0;
    margin-left: 160px;
    margin-right: 160px;
    /*background: #F5F5F5;*/
    font-family: 'Georgia', serif; 
    font-size: 18px; 
    color: #000;
}


h1 {
	font-family: Georgia, "Times New Roman", Times, serif; 
	border-bottom: 2px solid gray;
	color: #626456;
}

h2,h3,h4,h5,h6 {
	font-family: Georgia, "Times New Roman", Times, serif; 
	color: #8D8E85;
}

p {
	/*
	margin-top: 0.5em;
	line-height: 1.5em;
	font-size: 1.1em;
	*/
}

a {
	text-decoration: none;
	border-bottom: 1px dotted #B8D03B;
	color: #3C7BCF;
}

a:hover {
	border: none;
	background: #B8D03B;
	color: #FFFFFF;
}

pre {
  border: 1pt solid #AEBDCC;
  font-size: 0.8em;
  background-color: #F3F5F7;
  padding: 5pt;
  font-family: courier, monospace;
  white-space: pre;
  /* begin css 3 or browser specific rules */
  white-space: pre-wrap;
  word-wrap: break-word;
  white-space: -moz-pre-wrap;
  white-space: -pre-wrap;
  white-space: -o-pre-wrap;
  /* end css 3 or browser specific rules */
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
    