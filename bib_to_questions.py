import bibtexparser
from collections import Counter
import re
import plac

@plac.annotations(
    bib_file=("Location of .bib file", "option", "i", str),
    tag=("Tag to extract questions for", "option", "t", str))
def main(bib_file, tag):
    print("Extracting bibliographic entries from {0}".format(bib_file))
    with open(bib_file) as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)
    print("Bibliography has {0} total entries.".format(len(bib_database.entries)))

    all_q = []

    for i in bib_database.entries:
        ts = []
        if 'keywords' in i.keys():
            # clean up the tags; some are comma and some are semicolon sep
            ts = i['keywords'].replace(",", ";")
            ts = ts.split(";")
            ts = [i.strip() for i in ts]
        if 'annote' in i.keys() and tag in ts:
            questions = re.findall("Motivation\n(.+?)Argument", i['annote'], re.DOTALL)
            if questions:
                author = re.findall("^(.+?)\n", i['annote'], re.DOTALL)
                if author:
                    author = author[0].strip()
                if author == "One Sentence Summary":
                    print(i['ID'])
                questions = re.sub("--------------------\n\n", "", questions[0]).strip()
                if questions:
                    questions = questions.split("\n")
                    questions = [re.sub("^- ", "", i) for i in questions]
                    all_q.extend(questions)
    print("Found {0} entries for the tag '{1}'.".format(len(all_q), tag))
    for n, i in enumerate(all_q):
        print("{0}. {1}".format(n + 1, i))

if __name__ == "__main__":
    plac.call(main)
