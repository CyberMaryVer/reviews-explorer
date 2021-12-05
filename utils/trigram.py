import os
import pandas as pd
import streamlit as st
from mxnet import np, npx
from d2l import mxnet as d2l

npx.set_np()


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
        tokens = d2l.tokenize(df.loc[df.file == f].Link.values)
        corpus = [token for line in tokens for token in line]

        vocab = d2l.Vocab(corpus)
        uni_freqs[f] = vocab.token_freqs

        bigram_tokens = [pair for pair in zip(corpus[:-1], corpus[1:])]
        bigram_vocab = d2l.Vocab(bigram_tokens)
        bi_freqs[f] = bigram_vocab.token_freqs

        trigram_tokens = [triple for triple in zip(
            corpus[:-2], corpus[1:-1], corpus[2:])]
        trigram_vocab = d2l.Vocab(trigram_tokens)
        tri_freqs[f] = trigram_vocab.token_freqs

    return uni_freqs, bi_freqs, tri_freqs

