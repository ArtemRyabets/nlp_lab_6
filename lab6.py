import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, Input


def train_lstm_model():
    print("1. Завантаження даних (Loading data)...")
    try:
        df = pd.read_csv("kyiv_real_estate_PRO.csv")
    except FileNotFoundError:
        print("Помилка: Файл kyiv_real_estate.csv не знайдено!")
        return

    print("2. Попередня обробка тексту (Text preprocessing)...")
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['Category'])


    vocab_size = 5000
    max_length = 50

    tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['Text'])

    sequences = tokenizer.texts_to_sequences(df['Text'])
    padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

    X_train, X_test, y_train, y_test = train_test_split(padded_sequences, y, test_size=0.2, random_state=42)

    print("3. Створення LSTM архітектури (LSTM architecture creation)...")
    model = Sequential([

        Input(shape=(max_length,)),


        Embedding(vocab_size, 128),
        SpatialDropout1D(0.2),
        LSTM(100, dropout=0.2, recurrent_dropout=0.2),
        Dense(3, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    print("\n4. Початок навчання (Training start)...")

    history = model.fit(X_train, y_train, epochs=15, batch_size=16, validation_data=(X_test, y_test), verbose=1)

    print("\n5. Оцінка результатів (Evaluation)...")
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Точність моделі на тестових даних (Test Accuracy): {accuracy * 100:.2f}%")


if __name__ == "__main__":
    train_lstm_model()