
# Data System

System that eases taking and ordering notes.

## System Principles

- All data is stored in plain text files. It can be structured, but it should always be easy to see, understand and modify the data using a normal text editor. 
    - Does not mean there are not scripts to automate things, but fundamentally the data is the principal interface.

## System Design

    meta: try design principle: keep a very tight and concise data-model, defer implementation details.
    If the data-model is clear and complete, implementation can change independently and bad implementation will not influence and spill-over into the eventual convergence of the system.

- Every document has a unique ID.
  - Place where it renders to on the web is derivable from solely unique-ID.
    - What to do for document that CANNOT (e.j. require a different type of server) have this? Make sure unique-ID generates a page that then link to the external system.
- Need a metadata system to allocate and track those IDs.
- Documents can link to each-other by unique-ID, transformed into web link if public, reference section if private, error if reference to blank.
  - Make it possible / relatively easy for a documen to change unique-ID. Could be a script, or something that tracks all previous unique-ID and indicate when an "old link" is used.

- There is an inherent compromise between a system that is immediate (can always answer questions / can just be rendered on the fly) and a system that require a complete parse before questions can be answered. A good compromise could be in between where you do not need a parse to generate the documents (unlike now), but if any reference was newly introduced, it will fail and will not be fixed until the next complete parse. In this model, there is a metadata definition that contains the data from the last parse and is querried at runtime.

## Features Wanted

### Public AND Private

Want github-style use to be able to modify whenever I think of an idea or I have free time.
However, some stuff is provate. How to work with that.

Within the public mode, automatic publish to a website.

### Easy Capture

Can either parse an external tool (such as google keep) or work on word documents or whatever.
The goal is to allow to quickly take notes with metadata, allows the system to swallow those notes.

Have to be able to TAKE notes very easily, INCLUDING PICTURES. It is fine if it is eventually transformed in a mode that is harder to add pictures (for example .docx for collecting, eventually converting to makrdown + .png).

**The problem of easy capture and dating**. If I leverage other systems, I will most likely not have date of creation. A compromise (in the case where I did not enter it as a tag in-document).

#### The DataIzer: A Way to put Data in the System

Have a directory that can just accumulates files (e.g. /data_in). When a script is run, it destroys the original (well, place in a temp 'del me once in a while folder') and outputs document in a form that is understood by the system.

### Tag System

See mentioned in web/root.

### Reference and Save Refereed Work

- Any URL refered or reference used is parsed.

- Once parsed, another system gets a copy of the reference (.pdf or .html or whatever) and saves it in a data file.

The idea is to never be in a situation that you cannot find refered work because it has been 301'ed or censored. But at the same time it is painstaking and hard to keep track to have to manage manual copies.

Need to be able to be both in-document and external to document. If external then a .meta file applies for all documents in the folder (but not sub-folders). This set of files is seen as one document (the UID refers to the render page, but should be able to find the list of files in the master metadata manifest).

What is the UID for a document that is not formerly in he system (e.g. a .pdf file that I can't tag into)? Put uid_<uid> in the filename?

### Metadata

Create a metadata directory. Can be a set of JSON files.
Metadata covers both public and private, so be aware that tags and such are not private?

# TODO

## A

- Gather disparate code under this roof
    - docx to markdown
    - parse web
    - mine metadata

- Need to completely split the data system from the website. The website should be able to understand the output from the data-system, the dependency should only be from website to data system, not the inverse.

## B

- Move a bunch of disparate stuff (e.g. recipes or old reading notes) under the repository that is private.
