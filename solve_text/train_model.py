import pandas as pd
from keras import Sequential
from keras.src.layers import Dense, BatchNormalization
from keras.src.optimizers import Adam
from sklearn.model_selection import train_test_split

from solve_text.utils import prepare_df, get_vectors


def train_model():
    path = "../Data/PoemsDataset.csv"
    df = pd.read_csv(path)
    df = prepare_df(df)
    embedded_poems, encoded_labels, input_size, output_size = get_vectors(df)
    train_poems, test_poems, train_labels, test_labels = train_test_split(embedded_poems, encoded_labels, test_size=0.2)

    model = create_model(input_size, output_size)

    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    train_poems = train_poems.reshape(-1, 300)
    test_poems = test_poems.reshape(-1, 300)

    model.fit(train_poems, train_labels, batch_size=32, epochs=80)
    show_model_quality(model, test_poems, test_labels)
    model.save('sequential.keras')


def create_model(input_size, output_size):
    model = Sequential([
        Dense(units=128, input_dim=input_size, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=256, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=512, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=512, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=256, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=128, activation='relu'),
        # LeakyReLU(alpha=0.02),
        BatchNormalization(),
        Dense(units=output_size, activation='softmax')
    ])
    return model


def show_model_quality(model, test_poems, test_labels):
    test_loss, test_acc = model.evaluate(test_poems, test_labels)
    print(f'loss: {test_loss}, accuracy: {test_acc}')
    model.summary()


def main():
    train_model()


if __name__ == '__main__':
    main()
