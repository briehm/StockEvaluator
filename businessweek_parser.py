# -*- coding: utf-8 -*-

import urllib
import lxml.html
import requests
import nltk

import json
import document_metadata

from collections import Counter

def parse_businessweek_url(url):
    url = urllib.urlopen(url)
    url = url.geturl()

    page = requests.get(url)
    tree = lxml.html.fromstring(page.text)

    paragraphs = tree.xpath("//div[@id='article_body']//p/text()")

    article_text = "\n".join(paragraphs)
    return article_text


def tokenize_article(text):

    tokens = [t.lower() for t in nltk.word_tokenize(text)]

    clutter = {' ', '.', ',', ';', ':', '\n', '"', u"—", '[', ']', '(', ')', 'a', 'an', 'the'}

    all_bigrams = ((tokens[i],tokens[i+1]) for i in xrange(len(tokens)-1))
    cleaned_bigrams = [b[0]+"_"+b[1] for b in all_bigrams if b[0] not in clutter and b[1] not in clutter]

    return tokens, cleaned_bigrams


if __name__ == "__main__":

    urls = document_metadata.get_docs_by_source('Bloomberg').Weblink

    uni_counter = Counter()
    bi_counter = Counter()

    for url in urls[1:50]:
        text = parse_businessweek_url(url)
        unigrams, bigrams = tokenize_article(text)

        uni_counter.update(unigrams)
        bi_counter.update(bigrams)

    unigram_file = '/home/till/devel/python/hz15_tsdata/unigrams.json'
    bigram_file =  '/home/till/devel/python/hz15_tsdata/bigrams.json'

    with open(unigram_file, 'w') as fp:
        json.dump(dict(uni_counter), fp)

    with open(bigram_file, 'w') as fp:
        json.dump(dict(bi_counter), fp)

