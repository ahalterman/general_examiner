# general_examiner

Tools for studying for general exams

## Extracting information from notes

If notes are stored within a bibtex file's "annote" field using the format in
`note_template.txt`, these scripts can extract and structure information
contained in the fields. 


`bib_to_questions.py` takes in the location of a .bib file and returns all the
questions from the article notes matching that tag.

## Example usage

```
ahalterman:general_examiner$ python bib_to_questions.py -i /Users/ahalterman/MIT/MIT.bib -t "Civil War"
Extracting bibliographic entries from /Users/ahalterman/MIT/MIT.bib
Bibliography has 1116 total entries.
Found 15 entries for the tag 'Civil War'.
1. What is the effect of aid on civil conflict? Does it increase or decrease?
2. Does ethnic conflict cause civil war
3. Do economic shocks increase or decrease the probability of civil war?
4. Is there an ``opportunity cost'' mechanism in changing risk of war?
...
```


