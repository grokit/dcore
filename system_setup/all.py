
"""
Goal is to git clone dcore, then have all the scripts available and common functionalities run in cron.

# Todo: code this

- apt-get:
    vim
    git

- add PYTHONPATH dcore

- no dependencies on private_data (fix in other scripts)

- add to cron:
    report_to_cloud
    https_share (optional)
    files_index (daily)

## Cron

*/2 * * * * python3 /home/pi/dcore/apps/report_to_cloud/report_to_cloud.py
*/1 * * * * python3 /home/pi/dcore/apps/https_share/https_share.py -p 443 -s /home/pi/share -o /home/pi/share -a atoken_849h8ddj019
^^ must be in root's crontab
"""


