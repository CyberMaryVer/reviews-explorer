import pandas as pd
import streamlit as st
import nltk


nltk.download('punkt')


def get_corpus(df, sight_name):
    sight_df = df[df['sight'] == sight_name]
    lines = sight_df['review_text_rus'].tolist()
    tokens = []
    exceptions_count = 0
    tokenizer = nltk.RegexpTokenizer('\w+')
    for line in lines:
        try:
            tokens += tokenizer.tokenize(line)
        except Exception as exc:
            exceptions_count += 1
            if exceptions_count == 1:
                print(exc)
    return [token.lower() for token in tokens]


def get_uni_freqs(corpus):
    fdist = nltk.FreqDist(corpus)
    freqs = []
    for k, v in fdist.items():
        freqs.append((k, v))
    return freqs


def get_bi_freqs(corpus):
    bgs = nltk.bigrams(corpus)
    fdist = nltk.FreqDist(bgs)
    freqs = []
    for k, v in fdist.items():
        freqs.append((k, v))
    return freqs

def get_tri_freqs(corpus):
    tgs = nltk.trigrams(corpus)
    fdist = nltk.FreqDist(tgs)
    freqs = []
    for k, v in fdist.items():
        freqs.append((k, v))
    return freqs


@st.cache
def bigram_trigram(reviews_df):
    sight_names = reviews_df['sight'].unique()

    uni_freqs = {f: "" for f in sight_names}
    bi_freqs = {f: "" for f in sight_names}
    tri_freqs = {f: "" for f in sight_names}

    for sight_name in sight_names:
        corpus = get_corpus(reviews_df, sight_name)

        uni_freqs[sight_name] = get_uni_freqs(corpus)
        bi_freqs[sight_name] = get_bi_freqs(corpus)
        tri_freqs[sight_name] = get_tri_freqs(corpus)

    return uni_freqs, bi_freqs, tri_freqs
