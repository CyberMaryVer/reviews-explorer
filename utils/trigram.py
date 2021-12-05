import os
import pandas as pd
import streamlit as st
import re
# from mxnet import np, npx
# from d2l import mxnet as d2l

# npx.set_np()


def get_corpus(df, fname):
    tokens = re.split(r'\W+',
    '''
        Потрясающе! Совершенно необычное зрелище и год от года меняющееся. Можно ходить на этот вулкан каждый год и всегда будет интересно
    ''')
    tokens = [token for token in tokens if token != '']
    return tokens

    tokens = d2l.tokenize(df.loc[df.file == fname].Link.values)
    return [token for line in tokens for token in line]


def get_uni_freqs(corpus):
    return corpus[10:15]

    vocab = d2l.Vocab(corpus)
    return vocab.token_freqs


def get_bi_freqs(corpus):
    return [trigram for trigram in zip(corpus[5:10], corpus[6:])]

    bigram_tokens = [pair for pair in zip(corpus[:-1], corpus[1:])]
    bigram_vocab = d2l.Vocab(bigram_tokens)
    return bigram_vocab.token_freqs


def get_tri_freqs(corpus):
    return [trigram for trigram in zip(corpus[:5], corpus[1:], corpus[2:])]

    trigram_tokens = [triple for triple in zip(
        corpus[:-2], corpus[1:-1], corpus[2:])]
    trigram_vocab = d2l.Vocab(trigram_tokens)
    return trigram_vocab.token_freqs


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
