import bibtexparser
from collections import Counter
import re
import genanki
import plac

class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0] + self.fields[1])

cite_to_summ_model = genanki.Model(
  2020608274,
  'Citation to Summary',
  fields=[
    {'name': 'Citation'},
    {'name': 'Summary'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Citation}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Summary}}',
    }])

summ_to_cite_model = genanki.Model(
  2008369273,
  'Summary to Citation',
  fields=[
    {'name': 'Summary'},
    {'name': 'Citation'}
  ],
  templates=[
    {
      'name': 'Card 2',
      'qfmt': '{{Summary}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Citation}}',
    }])

def structure_note(note):
    title = re.findall("(.+)(?=One Sentence Summary)", note, flags = re.DOTALL)
    title = title[0].strip()
    author_year = re.findall("(.+?\d{4})", title)[0]
    summary = re.findall("(?<=One Sentence Summary\n)(.+?)(?=Question/Motivation)", note, flags = re.DOTALL)
    summary = re.sub("\-+?\n", "", summary[0])
    summary = summary.strip()
    return (author_year, summary)

def note_to_card(note_info, deck_internal):
    cts = MyNote(model=summ_to_cite_model, fields=[note_info[0], note_info[1]])
    #stc = MyNote(model=summ_to_cite_model, fields=[note[0], note[1]])
    deck_internal.add_note(cts)
    #summ_to_cite_deck.add_note(stc)

def tag_to_deck(bib_database, tag, reverse = False):
    # set up deck
    ### Use 10 digits of the tag's hash as the DB ID.
    ### Each deck needs to be unique, but keeping the same ID
    ###   allows decks to be updated in the future.
    tg = tag + str(reverse)
    print(tg)
    deck_id = abs(hash(tg)) % (10 ** 10)
    if reverse == True:
        deck_name = '{0}: Summary to Citation'.format(tag)
    else:
        deck_name = '{0}: Citation to Summary'.format(tag)
    deck_internal = genanki.Deck(deck_id, deck_name)

    # go through bib and make cards
    for i in bib_database.entries:
        ts = []
        if 'keywords' in i.keys():
            ts = i['keywords'].replace(",", ";")
            ts = ts.split(";")
            ts = [i.strip() for i in ts]
        if 'annote' in i.keys() and tag in ts:
            try:
                stuff = structure_note(i['annote'])
                if stuff[0] and stuff[1]:
                    if reverse:
                        stuff = (stuff[1], stuff[0])
                    note_to_card(stuff, deck_internal)
            except IndexError:
                print("Missing stuff for ", i['ID'])
    if reverse == True:
        fn = '{0}_sum_to_cite.apkg'.format(tag)
    else:
        fn = '{0}_cite_to_sum.apkg'.format(tag)
    genanki.Package(deck_internal).write_to_file(fn)
    print("Wrote deck to {0}".format(fn))

@plac.annotations(
    bib_file=("Location of .bib file", "option", "i", str),
    tag=("Tag to make cards for", "option", "t", str))
def main(bib_file, tag):
    print("Extracting bibliographic entries from {0}".format(bib_file))
    with open(bib_file) as bibtex_file:
        bibtex_str = bibtex_file.read()
    bib_database = bibtexparser.loads(bibtex_str)
    tag_to_deck(bib_database, tag)
    tag_to_deck(bib_database, tag, reverse = True)

if __name__ == "__main__":
    plac.call(main)
