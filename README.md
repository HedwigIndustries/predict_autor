# Predict author

#### Short description:

this project predicts which of the authors the poetic style of the poem is most similar to.

#### How it works?

First you need to parse the dataset of poems and authors , see ```parse/parse.py```.
The dataset will be saved in `Data`.

The ```selenium``` library is used for parsing

Let's prepare the training data, save prepared dataset in ```Data```.

Create text embedding, save ```FastText``` model with current text embedding.
Used libraries:
```keras```,
```numpy```,
```sklearn```,
see ```solve_text/utils```

Then we will create the ```Sequential``` model from the ```Keras``` library, train it on preprocessed data, save
model ```sequential.keras```,
see: ```solve_text/train_model.py```

Get name of author prediction for poem:```solve_text/poem.txt```, see `solve_text/predict_autor.py`.

