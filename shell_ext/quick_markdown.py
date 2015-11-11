
import codecs
import sys
import glob
import argparse

import markdown # 3rd party

"""
#TODO

"""

_meta_shell_command = 'markdown'

autoreplyJavascriptHeader = """
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
<b>Warning: enabled Markdown auto-refresh mode.</b>
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
html_pre_post = False

def do():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    args = parser.parse_args()
    
    files = []
    if args.filename is not None:
        files = [args.filename]
    
    if len(files) == 0:
        files += glob.glob('*.markdown')
        files += glob.glob('*.md')
        
    print("Using files: %s" % files)
    
    for file in files:
        fh = codecs.open(file, 'r', encoding="utf-8", errors="xmlcharrefreplace")
        mdstr = fh.read()
        fh.close()

        html = markdown.markdown(mdstr, ['fenced_code', 'codehilite'])

        filename = file + '.html'
        filename = filename.replace('.md', '')
        fh = codecs.open(filename, 'w', encoding='utf-8')
        
        print('Writing: %s.' % filename)
        if javanowing:
            fh.write(autoreplyJavascriptHeader + html + autor_post)
        elif html_pre_post:
            fh.write(html_pre + html + html_post)
        else:
            fh.write(html)
        fh.close()

if __name__ == "__main__":
    do()
    
