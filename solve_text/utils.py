from collections import Counter

import joblib
import numpy as np
from gensim.models import FastText
from keras.src.utils import to_categorical
from sklearn.preprocessing import LabelEncoder


def prepare_df(df):
    df = drop_punctuation(df)

    df = drop_not_letters(df)

    df = drop_short_poems(df)

    df = get_useful_words(df)

    df = drop_short_poems(df)
    df.to_csv('../Data/PreparedPoems.csv')
    return df


def get_useful_words(df):
    # drop uncommon words and very common words from poems
    unique_words = ' '.join(df['Poem']).split(' ')
    counts = Counter(' '.join(df['Poem']).split())
    common_words = set([word for word, _ in counts.most_common(int(len(unique_words) * 0.9))])
    very_common_words = set([word for word, _ in counts.most_common(int(len(unique_words) * 0.004))])
    df.loc[:, 'Poem'] = df['Poem'].apply(
        lambda poem: ' '.join([word if word in common_words and word not in very_common_words else ''
                               for word in poem.split()])
    )
    return df


def drop_short_poems(df):
    return df[df['Poem'].apply(lambda x: len(x) >= 20)]


def drop_not_letters(df):
    ru_alphabet = set(list('йцукенгшщзхъфывапролджэёячсмитьбю'))
    df['Poem'] = [''.join(list(filter(lambda ch: ch in ru_alphabet or ch == ' ', poem))) for poem in df['Poem']]
    return df


def drop_punctuation(df):
    df['Poem'] = [
        ''.join(ch if ch not in [';', ':', ','] else ' ' for ch in poem)
        .lower()
        .replace('\t', ' ')
        .replace('\n', ' ')
        .replace('\r', ' ')
        for poem in df['Poem']
    ]
    return df


def get_vectors(df):
    model = FastText(sentences=[poem.split() for poem in df['Poem']], vector_size=300, sg=1)
    model.save('fasttext.bin')

    embedded_poems = embedding_poems(model, df['Poem'])
    label_encoder, encoded_labels = encoding_labels(df['Autor'])

    return np.array(embedded_poems), encoded_labels, model.vector_size, len(label_encoder.classes_)


def encoding_labels(labels):
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)
    encoded_labels = to_categorical(encoded_labels)
    joblib.dump(label_encoder, 'label_encoder.joblib')
    return label_encoder, encoded_labels


def embedding_poems(model, poems):
    embedded_poems = []
    for poem in poems:
        embedded_poem = embedding_poem(model, poem)
        embedded_poems.append(embedded_poem)
    return embedded_poems


def embedding_poem(model, poem):
    word_vectors = [(model.wv[word]) for word in poem.split() if word in model.wv]
    if word_vectors:
        avg_vector = sum(word_vectors) / len(word_vectors)
        embedded_poem = avg_vector
    else:
        # if something wrong
        embedded_poem = [0.0] * model.vector_size
    return embedded_poem
