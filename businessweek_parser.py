# -*- coding: utf-8 -*-

import urllib
import lxml.html
import requests
import nltk


def parse_businessweek_url(url):
    # returns a tuple (headline, text)
    url = urllib.urlopen(url)
    url = url.geturl()
    page = requests.get(url)
    return parse_businessweek_html(page.text)

def parse_businessweek_file(filename):
    # returns a tuple (headline, text)
    try:
        with open(filename) as fp:
            return parse_businessweek_html('\n'.join(fp.readlines()))
    except IOError as ioe:
        return "", ""

def parse_businessweek_html(html_text):
    try:
        tree = lxml.html.fromstring(html_text)
    except:
        return "", ""

    headline = tree.xpath("//h1[@class='headline']/text()")
    headline = headline[0] if headline else ''
    paragraphs = tree.xpath("//div[@id='article_body']//p/text()")
    article_text = "\n".join(paragraphs).lower()
    return headline, article_text


def tokenize_article(text):

    tokens = [t.lower() for t in nltk.word_tokenize(text)]

    clutter = {' ', '.', ',', ';', ':', '\n', '"', u"—", '[', ']', '(', ')', 'a', 'an', 'the'}

    all_bigrams = ((tokens[i],tokens[i+1]) for i in xrange(len(tokens)-1))
    cleaned_bigrams = [b[0]+"_"+b[1] for b in all_bigrams if b[0] not in clutter and b[1] not in clutter]

    return tokens, cleaned_bigrams

def clean_company_name(name):
    name = name.lower()
    return name.strip()