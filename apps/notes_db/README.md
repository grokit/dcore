
# Overview

NotesDB: Take notes from a single Markdown file, and organize them in folders with metadata. Provide search utility which interprets metadata and folder structure (e.g. if search query in title, search will show before a note that has search query in body, search by tags, ...).

Guiding principles:

- All notes are kept as text in Markdown format.
- Short term notes are in injest.md file, allow for easy capture.
- Program transform _sections_ from injest.md into a note which has its own folder.
- In the folder of the note, feel free to add files, images, etc.
- The user is responsible for moving important notes to a different folder. Search will prioritize notes which are in the important folder.

# File and Folders Organization 
	
	$root/ingest.md: All notes captured go there. Feel free to copy / paste from your favorite note capturing tool (e.g. Word or Google Docs).

	$root/triage/$note: An parser automatically transfer ingest.md into separate notes (a single note boundary is defined by a top-level Markdown section denoted by the pound `#` character at the beginning of a line).


	$root/notes/$note

# Note Format and Metadata Conventions

Take notes in a single file, break down between notes with Markdown first-level section. Example:

	# Grocery List

	time::2016-08-02

	Bread
	Cheese

	# Meeting Notes

	time::2016-08-07
	tag::work

	Schedule less meetings.

This is interpreted as two different notes, and will end up in the following directories after the parser runs:

		$root/triage/2016-08-02_Grocery-List/note.md
		$root/triage/2016-08-07_Meeting-Notes/note.md

## Metadata

Metadata can be anywhere in the note and follows the format: 

	category::name(s)

For example:

	tag::work
	tag::vacation, bali
	time::2016-08-07
	
The note-taker application will automatically insert time metadata. If there is no time metadata, the parser will insert time-of-parse as time metadata.
	
# Parser

Title is in folder name, will be removed from note. All sections will go one-level down as result of parsing.

# Data-Entry

By default provide `nn` application (**N**ew **N**ote) which allows entering data from command line and automatically inserts time metadata.

# Swallowing Word Documents

User pandoc to convert .docx to Markdown. I have an utility that helps converting into a nicer note format, I may integrate with those scripts.

# Command-Line Utilities:

nn: New Note, Create a new note from command line, auto-add some metadata (e.g. time of creation) to the note.
sn: Search Notes, Search in notes.
in: Ingest Notes, Break-Down the ingest.md file into smaller notes which each get their own folder.
sc: Screenshot Copy, Put last screenshot take in ingest directory and link in ingest.md.


