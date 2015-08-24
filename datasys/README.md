
# Data System

System that eases taking, ordering and archiving notes.
Allows for effective search, editing and publishing.
Has in-built system for establishing and reviwing reviewing forefront.
Has in-built system for establishing and reviwing reviewing goals.

## System Principles

- All data is stored in plain text files. It can be structured, but it should always be easy to see, understand and modify the data using a normal text editor. 
    - Does not mean there are not scripts to automate things, but fundamentally the data is the principal interface.

- A document is a **folder**. A document folder is never nested (does not contain documents in sub-folders). Single files just get put in a folder, either named or generate folder name with UID. Reason for using folder is that is allows to easily append media to document and have option to "auto-add to appendix" and then move later for anythind that is not listed manually as link in markdown. Allows to just "put stuff that relates to that topic at that place".
    - Any tag or metadata in a file belonging to that document applies to the document as a whole.

- Everything is a document that has a UID. For cases like TheArchive.txt, it is just a different concept of a document that has a lot of sub-topic. This is idiosyncratic to this document, and it is fine to have such document which define funny structures as long as it folds to a document.

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

#### UID

What is the UID for a document that is not formerly in he system (e.g. a .pdf file that I can't tag into)? Put .uid_<uid>. in the filename? (e.g.: reading_notes.docx -> reading_notes.uid_8237291.docx)? Should UID be random number or just reflect the filename but that we know not to change?

Perhaps a good idea would be to always generate a random UID, but if it is change annotate as follows:
    uid::us828dh
    ... once I want to name my document:
    uid::us828dh=document_legible_uid
    
Now both uid will map to this document, can run a script to want all places that refer to the old one so that eventually can just remmove unused UIDs. But probably since the website URL

Important distinction: UID != URL. Each document can have > 1 URL and it is fine (although always have /uid/<uid> for all documents -- not recommended to have > 1 UID), the real UID is unique and always the rightmost in the uid declaration. Think of the previous UIDs as redirects. Should also be coded as a redirect as far as the web is concerned.

### Metadata

Create a metadata directory. Can be a set of JSON files.
Metadata covers both public and private, so be aware that tags and such are not private?

# Current System as it Is (Needs Reform)

- TheArchive.txt has misc topics, random notes. All mixed in. All have titles, but no organization beyond that.
- Some reading notes scattered on HD.
- Docx files left and right, some in google drive, some as archived content.
- Misc notes in google keep, usually important stuff is eventually folded in another document.
- A todo file + inbox keep track of current task "in next week / month".
- Some goal settings in calendar, journal, todo files. Sort of hap-hazard system of reviewing goals.
- No real tracking of rate of accomplishment of goals or rate of time investment.

## How To Reform System

-

# TODO

## A

- Gather disparate code under this roof
    - docx to markdown
    - parse web
    - mine metadata

- Need to completely split the data system from the website. The website should be able to understand the output from the data-system, the dependency should only be from website to data system, not the inverse.

## B

- Move a bunch of disparate stuff (e.g. recipes or old reading notes) under the repository that is private.
