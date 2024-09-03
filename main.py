import re
import sys
from pathlib import Path
from urllib.request import urlopen

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
from textwrap3 import fill

from lemmatizer import lemmatize_text


def selection(choice):
    if choice == 1:
        return "NABRE/NABRE Old Testament lemmatized"
    elif choice == 2:
        return "NABRE/NABRE 2nd Readings lemmatized"
    else:
        return "NABRE/NABRE Gospel lemmatized"


def norm(tokens):
    return [w.lower() for w in tokens if (w.isalpha() and w != "b")]


def main():
    analyze_date = input(
        "For Today's Date, type [T]. Otherwise, type the date in MMDDYY format"
    )
    if analyze_date == "T":
        url = "https://bible.usccb.org/daily-bible-reading"
    else:
        url = f"https://bible.usccb.org/bible/readings/{analyze_date}.cfm"
    data = urlopen(url).read().decode("utf8")
    soup = BeautifulSoup(data, features="html.parser")
    # content = soup.find(
    #     "div",
    #     class_="page-container node node--type-daily-reading node--promoted node--view-mode-full",
    # )
    readings = soup.find_all("div", class_="content-body")
    # Readings
    first_reading = readings[0]
    responsial_psalm = readings[1]
    second_reading = readings[2]
    alleluia = readings[3]
    gospel = readings[4]
    # Printing Readings
    print("*" * 80)
    print("First Reading")
    print("*" * 80)
    print(fill(first_reading.get_text(" "), 150))
    print("*" * 80)
    print("Responsial Psalm")
    print("*" * 80)
    print(fill(responsial_psalm.get_text(" "), 150))
    print("*" * 80)
    print("Second Reading")
    print("*" * 80)
    print(fill(second_reading.get_text(" "), 150))
    print("*" * 80)
    print("Alleluia")
    print("*" * 80)
    print(fill(alleluia.get_text(" "), 150))
    print("*" * 80)
    print("Gospel")
    print("*" * 80)
    print(fill(gospel.get_text(" "), 150))
    # User Choice For Analysis
    choice = input(
        "Which would you like to analyze: [1] for 1st Reading [2] for 2nd Reading [3] for Gospel"
    )
    choice = int(choice)
    text = readings[(choice - 1) * 2].get_text(" ")
    folder = selection(choice)
    corpus = PlaintextCorpusReader(folder, ".*")
    # Downloading Text to Separate Folder
    # Downloading Text to Separate Folder
    text = re.sub("\n", "", text)
    text = re.sub("  ", " ", text)
    text = re.sub("[^\x00-\x7f]", "", text)
    text = re.sub("( [A-Z]+ )", "", text)
    text = re.sub("\[ [a-z]+ \]", "", text)
    text = re.sub(r"[0-9]*\xa0", "", text)
    text = re.sub(r"[0-9]*\[a-zA-Z]*[0-9]*", "", text)
    text = re.sub(r"\[[a-zA-z]*\]", "", text)
    text = lemmatize_text(text)
    text = text.encode("utf-8")
    new_folder = Path("Text")
    filename = new_folder / "todays_text.txt"
    new_folder.mkdir(exist_ok=True)
    with open(filename, "w") as f:
        print(text, file=f)
    # Loading in tokenized Text
    analysis_words = PlaintextCorpusReader("Text", ".*\.txt")
    analysis_words = analysis_words.words()
    text_norm = norm(analysis_words)
    corpus_norm = norm(corpus.words())

    # Example frequency distributions
    text_freq = nltk.FreqDist(text_norm)
    corpus_freq = nltk.FreqDist(corpus_norm)

    # Bigram association measures
    bigram_measures = nltk.collocations.BigramAssocMeasures()

    # Initialize a frequency distribution for keyness
    keyness = nltk.FreqDist()

    # Calculate keyness score for each word in text_freq
    for w in text_freq:
        # Avoid division by zero and negative values
        text_count = text_freq[w]
        corpus_count = corpus_freq[w]

        # Calculate expected frequency safely
        if corpus_freq.N() > 0:
            expected_freq = (text_freq.N() / corpus_freq.N()) * corpus_count
        else:
            expected_freq = 0

        # Only compute keyness if text_freq[w] is greater than expected_freq
        if 0 < expected_freq < text_count:
            try:
                # Compute the likelihood ratio
                likelihood_ratio = bigram_measures.likelihood_ratio(
                    text_count, (corpus_count, text_freq.N()), corpus_freq.N()
                )
                keyness[w] = likelihood_ratio
            except ValueError as e:
                print(f"ValueError: {e} for word '{w}'")
                keyness[w] = 0  # Handle exception by setting keyness to zero
    scores = int(input("How many keywords would you like?"))
    # Get the top 25 keyness scores
    top_scores = keyness.most_common(scores)

    # Print the results
    print(f"Top {scores} keyness scores:")
    for word, score in top_scores:
        print(f"{word}: {score}")


if __name__ == "__main__":
    sys.exit(main())
