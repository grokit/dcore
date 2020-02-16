
# TODO -- foreword

This is a list of random ideas.
Sometimes I go through and pick a good one.

# TODO

- !! should still be able to ingest specific file -> if just file, create a default folder with file and filename as title with appropriate tag

- Auto do it from any folder.
- Before and after: commit to git


- Score includes last modified time
    - DONE, but allow to sort JUST with time
- List by tags
    - By tags and time

nn allow to list and filter by tags
AND list by modified time WITH non-trivial tags

nn:: take whole dire and make a note out of it
    nn --dir . <title>

ez to code:
    build dashboard with all todo:::a, b
    send my mail if not empty
    SUPER QUICK HACK: do it immediately!


ns super useful idea:
    restrict search to tag
    ns 'nethogs' --> ns -t linux nethogs
    ns -t now project

    support vi open a set of uuids:

    ns -b something
    bucket:::luid1, luid2, ...

nn: ingest should ingest WO having to be in proper folder. should do git before and after automatically.

nn: insert date after first pound

- More search points if:
    - Search is in title
    - Has UUID
    - Has tag
    - Had an `important` or `todo` tag.

- critical.sh -> proper python script -- maybe produce html page.

- nn --sshot or something like that: copy last screenshot or last 1 hour screenshot to dir with last touched note.md file.

- nn -l --last: open last modified note.md
- nn --recent: last 10 by modified time, option to open any of them
    | tocb -> toclipboard
    --> put all output in clipboard, have a mode to select line by line (0....n): just input the line want to copy in cliipboard.
    !!!! ns -f <whatever>  <-- just output the file instead of opening in vim. Use to open within vim.
dcore: hsearch: regex search bash history
dcore: clipboard manipulator (0-10: pick line to put in clipboard)
    ^^ extract files and folders

tag:-:now support

    in doc:
want to be able to enter in gdoc or any mode of entry where my system is not available (mail, etc).
pragmatic programmer: use text as format, make changing possible 
    ns -F
    ^^ same as -O but just output the single file so that it can be used in vim:
    !e ns -F vim
    score: take into account when file last modified
    take into account modified frequency (can infer from git)
    should have an option to order result chronologically. or at least boost by chronology
    ingest --task <file.md> -> file as task
    ingest --task_complete <folder>

    ingest here: create in current directory instead of "low"

ns: penalize if /meh is in path
    if `meh` in filename of folder, penalize
++ consider path in search

if tag:::important --> HIGHER SCORE

ns: BUILD THE DASHBOARD. TODO:::A should be unbreak-now (in red)
ns <x> -c0 : just display match line with nothing else
ns -o: don't print, just show choices
python install: bashrc / profile: at one place not the same, just generalize
find . | grep tata | save
save: configurable, by default goes in a folder, picking a new name

if search term anywhere in UUID, it's a big deal

Reorgnize new structure:
    - parse.py
        - article -> content, titles, tags, uuid
    - search.py
        - return (rank, note-path)
    - cmdline/ 
        - all commands and shortcuts
    - mutate.py
        - append, fix metadata, move, ...

- generalize shortcuts (no .basrc stuff), put all of them in ./commandline or something like that. 
-> nowa, nowb, nowc, now

- See other TODOs in individual python files as well.

tags
    tag[SEP]now --> $ now either opens only one or list 
    could make generic with topen <tag>
    tag lost

ns --list-tags
    List all tags and popularity.
    --uuid list of uuids

t <t number>: create / open task folder
ns -> sn `search notes`
ns -l 10: list last 10 folders in `low`. Also: task?
instead of uuid:::now, use tag:::now and allow > 1 with selection (/w default open most recently modified)
tag:::wait
complete task button: move from task to low, with tag `completed task` and add date if not there
low: don't search beyond 3 months, older it is, lower score it gets
had tag:::important: + ranking
movenow: move to folder that has now. Can do that with any search folder (think how to consolidate).
file <folder>: move to low, preprend date if not already exist

notes:
    refactor such that can know every score comes from which rule (class-like with name)
    only lookback 3 months for low
    kvp list, tag list <-- all in same meta package
