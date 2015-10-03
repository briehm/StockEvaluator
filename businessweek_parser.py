# -*- coding: utf-8 -*-

import urllib
import lxml.html
import requests
import nltk


def parse_businessweek_url(url):
    url = urllib.urlopen(url)
    url = url.geturl()
    page = requests.get(url)
    return parse_businessweek_html(page.text)

def parse_businessweek_file(filename):
    with open(filename) as fp:
        return parse_businessweek_html('\n'.join(fp.readlines()))

def parse_businessweek_html(html_text):
    tree = lxml.html.fromstring(html_text)
    paragraphs = tree.xpath("//div[@id='article_body']//p/text()")
    article_text = "\n".join(paragraphs).lower()
    return article_text


def tokenize_article(text):

    tokens = [t.lower() for t in nltk.word_tokenize(text)]

    clutter = {' ', '.', ',', ';', ':', '\n', '"', u"—", '[', ']', '(', ')', 'a', 'an', 'the'}

    all_bigrams = ((tokens[i],tokens[i+1]) for i in xrange(len(tokens)-1))
    cleaned_bigrams = [b[0]+"_"+b[1] for b in all_bigrams if b[0] not in clutter and b[1] not in clutter]

    return tokens, cleaned_bigrams

def clean_company_name(name):
    name = name.lower()
    return name.strip()