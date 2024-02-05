import joblib
import numpy as np
from gensim.models import FastText
from keras.models import load_model

from solve_text.utils import embedding_poem


def solve_poem():
    with open('poem.txt', 'r', encoding='utf-8') as f:
        poem = f.read()
    model = FastText.load('fasttext.bin')
    embedded_poem = embedding_poem(model, poem)
    predict(embedded_poem)


def predict(poem):
    model = load_model('sequential.keras')
    prediction = model.predict(np.array([poem]))
    print(prediction)
    class_indices = np.argmax(prediction, axis=1)
    loaded_label_encoder = joblib.load('label_encoder.joblib')
    autor = loaded_label_encoder.inverse_transform(class_indices)
    print(f'Text seems like autor: {autor}')


def main():
    solve_poem()


if __name__ == '__main__':
    main()
