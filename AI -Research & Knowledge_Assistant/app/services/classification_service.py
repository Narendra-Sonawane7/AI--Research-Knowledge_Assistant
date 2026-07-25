import os
import numpy as np
import tensorflow as tf

CATEGORIES = [
    "Artificial Intelligence",
    "Machine Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Robotics",
    "Cyber Security",
    "Cloud Computing",
]

MODEL_PATH = "./app/ml_saved_model.keras"


def build_and_train_dummy_model():
    texts = [
        "This paper discusses neural networks and transformers",
        "A study on image detection and segmentation",
        "Cloud architecture and deployment strategy",
        "Network attack detection and secure systems",
        "Robot navigation and control",
        "Text classification and language understanding",
        "Supervised learning and regression methods",
    ]
    labels = [0, 2, 6, 5, 4, 3, 1]

    vectorizer = tf.keras.layers.TextVectorization(
        max_tokens=1000,
        output_mode="tf_idf"
    )
    vectorizer.adapt(texts)

    model = tf.keras.Sequential([
        tf.keras.Input(shape=(1,), dtype=tf.string),
        vectorizer,
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(len(CATEGORIES), activation="softmax"),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    x_train = tf.constant(texts, dtype=tf.string)
    y_train = tf.constant(labels, dtype=tf.int32)

    model.fit(x_train, y_train, epochs=5, verbose=0)
    model.save(MODEL_PATH)
    return model


def load_model():
    if os.path.exists(MODEL_PATH):
        return tf.keras.models.load_model(MODEL_PATH)
    return build_and_train_dummy_model()


def classify_text(text: str):
    model = load_model()
    pred = model.predict(tf.constant([text], dtype=tf.string), verbose=0)[0]
    idx = int(np.argmax(pred))
    return {
        "category": CATEGORIES[idx],
        "confidence": float(pred[idx]),
    }