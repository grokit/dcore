upload_body = r"""
<h2>Upload Form</h2>

<p>Trust us, we will make good use of that data.</p>

<p><b>THERE IS A KNOWN BUG IN THE UPLOAD WHICH SOMETIMES CORRUPT FILES. Don't upload here until fixed :).</b></p>

<form enctype="multipart/form-data" action="/upload/sink/" method="POST">
Choose a file to upload: <input name="uploadedfile" type="file" />
<input type="submit" value="Upload File" />
</form>"""

main_html = r"""
<p>
<a href="/files/">List files</a><br>
<a href="/upload/">Upload</a><br>
<a href="/log/">See server logs</a><br>
</p>
"""

html_template = """
<head>
__head__
</head>

<style type=text/css>
__style__
</style>
  
<html>
<body>

__body__

__debug_info__
<body>
</html>
"""

main_log = r"""
<p>
<pre><code>
{0}
</code></pre>
</p>
"""

not_auth_body = r"""
<h2>401 Unauthorized</h2>

<p>
You need an access token to access this website.

<form action="/set_cookie/">
  Access Token: <input type="text" name="accessToken"><input type="submit" value="Submit">
</form>
</p>
"""

not_auth_folder_body = r"""
<h2>401 Unauthorized</h2>

<p>
You do not have access to this resource: __resource__.
</p>
"""
