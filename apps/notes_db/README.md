
# TODO

## As

DCORE_SECTION_BEGIN should be at END of .bashrc

ns: penalize if /meh is in path
    if `meh` in filename of folder, penalize
++ consider path in search

- generalize shortcuts (no .basrc stuff), put all of them in ./commandline or something like that. 
-> nowa, nowb, nowc, now

ls | dclip -s
--> select by line
 
if tag:::important --> HIGHER SCORE
stable sort

ns: BUILD THE DASHBOARD. TODO:::A should be unbreak-now (in red)
ns: biggest issue right now is non-stable sort
ns <x> -c0 : just display match line with nothing else
ns -o: don't print, just show choices
python install: bashrc / profile: at one place not the same, just generalize
find . | grep tata | save
save: configurable, by default goes in a folder, picking a new name

Reorgnize new structure:
    - parse.py
        - article -> content, titles, tags, uuid
    - search.py
        - return (rank, note-path)
    - cmdline/ 
        - all commands and shortcuts
    - mutate.py
        - append, fix metadata, move, ...


## Bs

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

# Overview

NotesDB: Take notes from a single Markdown file, and organize them in folders with metadata. Provide search utility which interprets metadata and folder structure (e.g. if search query in title, search will show before a note that has search query in body, search by tags, ...).

Guiding principles:

- All notes are kept as text in utf8, human-readeable format. Right now using Markdown++.
- Program transform _sections_ from injest.md into a note which has its own folder.
- In the folder of the note, feel free to add files, images, etc.
- The user is responsible for moving important notes to a different folder. Search will prioritize notes which are in the important folder.

Addressed scenarios:

- Just want to take a quick note that is searcheable later, want note sytem to automatically append date and file. Should be easy to add different tags for later search.
- Support for long-lived articles as well as ad-hoc notes.
- Search in body of notes, order match with metadata (similar to google: more likely to be a match if other high quality nodes refer it, ...).
- Do not impose a lot of rules, let every note be a folder and user is free to add data to that folder.
- Link between notes.
- Easy to sync over git, mostly text files, other data (images, files) are not trapped in the system.
- Keep todo list from single todo markers in disparate files.
- Support todo list.
- Can open from anywhere in console, easy for quick-edit.

# File and Folders Organization 
	
	/ingest.md: All notes captured go there. Feel free to copy / paste from your favorite note capturing tool (e.g. Word or Google Docs).
    
    ::::::TODO: replace low -> auto
    /low/: Notes go there by default.
    
    /articles/: Move things there that are more important.

    /tasks/: Thins currently being worked on.

# Note Format and Metadata Conventions

Take notes in a single file, break down between notes with Markdown first-level section. Example:

	# Grocery List

	time:::2016-08-02

	Bread
	Cheese

	# Meeting Notes

	time:::2016-08-07
	tag:::work

	Schedule less meetings.

This is interpreted as two different notes, and will end up in different directories after `ingest` is run on them.

## Metadata

Metadata can be anywhere in the note and follows the format: 

	category:::name(s)

For example:

	tag:::work
	tag:::vacation, bali
	time:::2016-08-07
	
The note-taker application will automatically insert time metadata. If there is no time metadata, the parser will insert time-of-parse as time metadata.

All metadata in the `category:::name` format is kept on the same line. This is to allow search using `ack` or `ag` if search.py is not convenient for you.

### Metadata: Tag 

After the tag marker:

- wait: something that needs to be revisited.
- wait-<whatever>
- todo
- todo-<priority-lexicographical>
- now: only keep a few documents that you are currently working on with this tag. Can be opened quickly by searching tag.
- important: will get scored higher in search.
- merge: will auto-merge with an article (will offer a selection).
- merge-<x>: x will be search to filter-down the list of articles it can be merged with.

Might want to eventually have a cron job which outputs a webpage in a ./dashboard folder, goal would be to review every other day.

### Metadata: UUID

UUID has this form: `uuid:::notes_db_readme`.

A UUID is _unique_: cannot have the same UUID on more than one document. However, a document can have multiple UUIDs. The reason for that is to allow UUID renames. UUID are used in order to publish on the web, so want to be able to rename and have two URLs point to the same document. For example:

    uuid:::notes_db, notes_db_better

In this case, both `notes_db` and `notes_db_better` uniquely identify the document. The last uuid is deemed to be the most recent, so for URLs could redirect all UUIDs which is not the last one listed using a 301 to the URL of the las UUID.

UUIDs links:

    luid:::notes_db
    link-uuid:::notes_db

Both mean exactly the same thing. Use in order to have a link to another document by UUID.
Note that luid is missing a u intentionally in order not to turn up in a grep-search.

# Parser

Title is in folder name, will be removed from note. All sections will go one-level down as result of parsing.

# Data-Entry

By default provide `nn` application (**N**ew **N**ote) which allows entering data from command line and automatically inserts time metadata.

# Swallowing Word Documents

User pandoc to convert .docx to Markdown. I have an utility that helps converting into a nicer note format, I may integrate with those scripts.

# Command-Line Utilities:

    nn: New Note, Create a new note from command line, auto-add some metadata (e.g. time of creation) to the note.
    sn: Search Notes, Search in notes.
    sn -o: Search Notes Open, Search in notes, for all filenames that matched, offer to open in text editor.
    in: Ingest Notes, Break-Down the ingest.md file into smaller notes which each get their own folder.
    sc: Screenshot Copy, Put last screenshot take in ingest directory and link in ingest.md.

