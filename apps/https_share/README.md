**Most up-to-date information about this project at: [http://www.grokit.ca/cnt/HttpsShare/](http://www.grokit.ca/cnt/HttpsShare/). Use this page just to get the code :).**

This script allows you to securely share files over HTTPS.

You simply start the script using the following:

    python3 https_share.py -a magic-access-token_fj9efd3c -p 4443

Now, you need the magic token in order to access the files. If you access the https URL without setting the magic token first, you will get a '401 Unauthorized'. In order to set the token, simply go to:

    https://whatever/set_token/magic-access-token_fj9efd3c
    https://whatever/

Obviously replace the magic token by the same one you used when the application started. This token will be saved as a cookie and now you can now access the files! 

The usecase for this script is to share files between computers without risking having someone unauthorized getting access. It uses TLS so all the traffic will be encrypted.

![screenshot](https://github.com/nothing1212/https_share/blob/master/sshot2.png?raw=true)
