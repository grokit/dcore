
import new_note

note = open('./test/input/ingest.md').read()
new_note.ingest(note, './test/output')
