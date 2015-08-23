
# Data System

System that eases taking and ordering notes.

## System Design

- Every document has a unique ID.
  - Place where it renders to on the web is derivable from solely unique-ID.
    - What to do for document that CANNOT (e.j. require a different type of server) have this? Make sure unique-ID generates a page that then link to the external system.
- Need a metadata system to allocate and track those IDs.
- Documents can link to each-other by unique-ID, transformed into web link if public, reference section if private, error if reference to blank.
  - Make it possible / relatively easy for a documen to change unique-ID. Could be a script, or something that tracks all previous unique-ID and indicate when an "old link" is used.

## Features Wanted

### Public AND Private

Want github-style use to be able to modify whenever I think of an idea or I have free time.
However, some stuff is provate. How to work with that.

Within the public mode, automatic publish to a website.

### Easy Capture

Can either parse an external tool (such as google keep) or work on word documents or whatever.
The goal is to allow to quickly take notes with metadata, allows the system to swallow those notes.

Have to be able to TAKE notes very easily, INCLUDING PICTURES. It is fine if it is eventually transformed in a mode that is harder to add pictures (for example .docx for collecting, eventually converting to makrdown + .png).

### Tag System

See mentioned in web/root.

### Reference and Save Refereed Work

- Any URL refered or reference used is parsed.

- Once parsed, another system gets a copy of the reference (.pdf or .html or whatever) and saves it in a data file.

The idea is to never be in a situation that you cannot find refered work because it has been 301'ed or censored. But at the same time it is painstaking and hard to keep track to have to manage manual copies.

# TODO

## A
## B
