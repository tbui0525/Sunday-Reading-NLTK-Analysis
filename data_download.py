import re
import sys
from pathlib import Path
from urllib.request import urlopen

from bs4 import BeautifulSoup


def cleanse(new_folder, new_url):
    new_data = urlopen(new_url).read().decode("utf-8")
    nsmbu = BeautifulSoup(new_data)
    dlc = nsmbu.find("div", class_="version-NABRE result-text-style-normal text-html")
    header = nsmbu.find("h2")
    if header:
        header = header.get_text(" ")
    subheader = nsmbu.find("h3")
    if subheader:
        subheader = subheader.get_text(" ")
    subsubheader = nsmbu.find("h4")
    if subsubheader:
        subsubheader = subsubheader.get_text(" ")
    verses = dlc.get_text(" ")
    footnotes = nsmbu.find("ol")
    crossrefs = nsmbu.find("div", class_="crossrefs hidden")
    if footnotes:
        dawgs = footnotes.get_text(" ")
        verses = verses.replace(dawgs, "", 1)
    if crossrefs:
        criss = crossrefs.get_text(" ")
        verses = verses.replace(criss, "", 1)
    verses = verses.replace("Footnotes", "")
    verses = re.sub("\( [A-Z]+ \)", "", verses)
    verses = re.sub("\[ [a-z]+ \]", "", verses)
    verses = re.sub(r"[0-9]*\xa0", "", verses)
    verses = re.sub("”", "", verses)
    verses = re.sub("“", "", verses)
    verses = re.sub("‘", "", verses)
    verses = re.sub("’", "", verses)
    verses = re.sub(r"\n", "", verses)
    if header:
        verses = re.sub(header, "", verses)
    if subheader:
        verses = re.sub(subheader, "", verses)
    if subsubheader:
        verses = re.sub(subsubheader, "", verses)
    section = nsmbu.find_all("b", class_="inline-h3")
    for i in range(0, len(section)):
        verses = verses.replace(section[i].get_text(" "), "", 1)
    verses = verses.encode("utf-8")
    file = nsmbu.find("div", class_="dropdown-display-text").get_text(" ")
    filename = new_folder / (file + ".txt")
    new_folder.mkdir(exist_ok=True)
    with open(filename, "w") as f:
        print(verses, file=f)
    new_url = new_url[0:28] + nsmbu.find(class_="next-chapter")["href"]
    return new_url


def main():
    folder = Path("NABRE/NABRE Old Testament")
    new_url = "https://www.biblegateway.com/passage/?search=Genesis%201&version=NABRE"
    while "Matthew" not in new_url:
        cleanse(folder, new_url)
    folder = Path("NABRE/NABRE Gospel")
    new_url = "https://www.biblegateway.com/passage/?search=Matthew%201&version=NABRE"
    while (
        ("Matthew" in new_url)
        or ("Mark" in new_url)
        or ("Luke" in new_url)
        or ("John" in new_url)
    ):
        cleanse(folder, new_url)
    folder = Path("NABRE/NABRE 2nd Readings")
    new_url = "https://www.biblegateway.com/passage/?search=Acts%201&version=NABRE"
    while new_url:
        cleanse(folder, new_url)
    return


if __name__ == "__main__":
    sys.exit(main())
