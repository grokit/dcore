"""
Use this script to update part of files between mark.
For example:

MyFile.txt:

    Something.

    BEGIN
    theBird=12
    END

    Something else.

update('MyFile.txt', 'BEGIN', 'END', 'theBird=14')
Would update everything between the begin and end marker with the string provided as the last parameter.
"""
