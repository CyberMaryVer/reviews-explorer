import os
import pandas as pd
import streamlit as st
import nltk


nltk.download('punkt')


def get_corpus(df, fname):
    lines = df.loc[df.file == fname].Link.values
    tokens = []
    exceptions_count = 0
    tokenizer = nltk.RegexpTokenizer('\w+|\$[\d\.]+|\S+')
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
def bigram_trigram():
    filenames = [f for f in os.listdir("./data") if "main" not in f]
    files = [os.path.join("data", f) for f in os.listdir("./data") if "main" not in f]
    df = pd.DataFrame()

    for f, fname in zip(files, filenames):
        print(f)
        dff = pd.read_csv(f)
        dff["file"] = fname
        df = pd.concat((df, dff))

    uni_freqs = {f: "" for f in filenames}
    bi_freqs = {f: "" for f in filenames}
    tri_freqs = {f: "" for f in filenames}

    for f in filenames:
        corpus = get_corpus(df, f)

        uni_freqs[f] = get_uni_freqs(corpus)
        bi_freqs[f] = get_bi_freqs(corpus)
        tri_freqs[f] = get_tri_freqs(corpus)

    return uni_freqs, bi_freqs, tri_freqs
