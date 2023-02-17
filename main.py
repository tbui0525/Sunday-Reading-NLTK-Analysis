import nltk
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import re
from textwrap3 import fill
from nltk.corpus import PlaintextCorpusReader
def selection(choice):
    if choice == 1:
        return "NABRE/NABRE Old Testament"
    elif choice == 2:
        return "NABRE/NABRE 2nd Readings"
    else:
        return "NABRE/NABRE Gospel"
def norm(tokens):
    return [w.lower() for w in tokens if (w.isalpha() and w != 'b')]
def main():
    url = 'https://bible.usccb.org/bible/readings/021923.cfm'
    data = urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(data, features ="html.parser")
    content = soup.find('div',
                        class_='page-container node node--type-daily-reading node--promoted node--view-mode-full')
    readings = soup.find_all('div', class_='content-body')
    #Readings
    first_reading = readings[0]
    responsial_psalm = readings[1]
    second_reading = readings[2]
    alleluia = readings[3]
    gospel = readings[4]
    #Printing Readings
    print("*"*80)
    print("First Reading")
    print("*"*80)
    print(fill(first_reading.get_text(' '), 150))
    print("*" * 80)
    print("Second Reading")
    print("*" * 80)
    print(fill(second_reading.get_text(' '), 150))
    print("*" * 80)
    print("Gospel")
    print("*" * 80)
    print(fill(gospel.get_text(' '), 150))
    #User Choice For Analysis
    choice = input("Which would you like to analyze: [1] for 1st Reading [2] for 2nd Reading [3] for Gospel")
    choice = int(choice)
    text = readings[(choice-1)*2].get_text(' ')
    folder = selection(choice)
    corpus = PlaintextCorpusReader(folder, '.*')
    #Downloading Text to Separate Folder
    sents = nltk.sent_tokenize(text)
    v = []
    for sen in sents:
        sent = re.sub("\n", "", sen)
        sent = re.sub("  ", " ", sen)
        v.append(sent)
    toks = [nltk.word_tokenize(sent) for sent in v]
    tagger = nltk.tag.perceptron.PerceptronTagger()
    tagged = [tagger.tag(sent) for sent in toks]
    folder = Path('Text')
    filename = folder/ ('todays_text.txt')
    folder.mkdir(exist_ok = True)
    with open(filename, 'w') as f:
        for sent in tagged:
            for w,t in sent:
                print(w,t, sep='_', end= ' ', file = f)
            print(file = f)
    #Loading in tokenized Text
    tagged_text = nltk.corpus.reader.TaggedCorpusReader('Text/', r'[^.].*\.txt', sep = '_')
    text = tagged_text.words()
    #Corpus and Text Normalization
    text_norm = norm(text)
    corpus_norm = norm(corpus.words())
    #Keyness measurement
    text_freq = nltk.FreqDist(text_norm)
    corpus_freq = nltk.FreqDist(corpus_norm)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    keyness = nltk.FreqDist()
    for w in text_freq:
        if text_freq[w] > (text_freq.N()/corpus_freq.N()*corpus_freq[w]):
            keyness[w] = bigram_measures.likelihood_ratio(text_freq[w],
                                                           (corpus_freq[w], text_freq.N()), corpus_freq.N())
    top_25 =keyness.most_common(25)
    for x, y in top_25:
        print(f"{x} {y}")

if __name__ == "__main__":
    sys.exit(main())