"""
http://stackoverflow.com/questions/7333232/concatenate-two-mp4-files-using-ffmpeg
$ cat mylist.txt
file '/path/to/file1'
file '/path/to/file2'
file '/path/to/file3'

$ ffmpeg -f concat -i mylist.txt -c copy output
"""
