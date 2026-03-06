import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

def transformer_model():

    inputs = tf.keras.Input(shape=(60,1))

    x = layers.MultiHeadAttention(num_heads=4,key_dim=16)(inputs,inputs)

    x = layers.GlobalAveragePooling1D()(x)

    x = layers.Dense(64,activation="relu")(x)

    outputs = layers.Dense(1,activation="sigmoid")(x)

    model = tf.keras.Model(inputs,outputs)

    model.compile(optimizer="adam",loss="binary_crossentropy")

    return model


def transformer_predict(df):

    model = transformer_model()

    data = df["close"].values

    X = []

    for i in range(60,len(data)):

        X.append(data[i-60:i])

    X = np.array(X)

    X = X.reshape(X.shape[0],X.shape[1],1)

    pred = model.predict(X[-1].reshape(1,60,1))

    if pred > 0.5:
        return "buy"
    else:
        return "sell"