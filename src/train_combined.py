
import os
import sys
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

np.random.seed(42)
tf.random.set_seed(42)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_combined.csv")

def load_and_preprocess_data(data_path):
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    texts = df['Complaint_Text'].fillna('').values
    departments = df['Category'].values
    severities = df['Severity'].values
    
    dept_encoder = LabelEncoder()
    dept_labels = dept_encoder.fit_transform(departments)
    
    severity_encoder = LabelEncoder()
    severity_labels = severity_encoder.fit_transform(severities)
    
    return texts, dept_labels, severity_labels, dept_encoder, severity_encoder

def create_model(num_dept_classes, num_severity_classes, vocab_size, max_length):
    inputs = keras.Input(shape=(max_length,))
    x = layers.Embedding(vocab_size, 64)(inputs)
    x = layers.Bidirectional(layers.LSTM(64))(x)
    x = layers.Dense(64, activation='relu')(x)
    
    dept_output = layers.Dense(num_dept_classes, activation='softmax', name='department_output')(x)
    severity_output = layers.Dense(num_severity_classes, activation='sigmoid', name='severity_output')(x)
    
    model = keras.Model(inputs=inputs, outputs=[dept_output, severity_output])
    model.compile(
        optimizer='adam',
        loss={
            'department_output': 'sparse_categorical_crossentropy',
            'severity_output': 'binary_crossentropy'
        },
        metrics={'department_output': 'accuracy', 'severity_output': 'accuracy'}
    )
    return model

def main():
    texts, dept_labels, severity_labels, dept_encoder, severity_encoder = load_and_preprocess_data(DATA_PATH)
    
    print(f"Loaded {len(texts)} complaints")
    print("Department classes:", dept_encoder.classes_)
    print("Severity classes:", severity_encoder.classes_)
    
    # Split data
    train_val_texts, test_texts, train_val_dept, test_dept, train_val_sev, test_sev = train_test_split(
        texts, dept_labels, severity_labels, test_size=0.2, random_state=42, stratify=severity_labels
    )
    
    train_texts, val_texts, train_dept, val_dept, train_sev, val_sev = train_test_split(
        train_val_texts, train_val_dept, train_val_sev, test_size=0.1, random_state=42
    )
    
    # Vectorize
    vectorizer = layers.TextVectorization(max_tokens=10000, output_mode='int', output_sequence_length=100)
    vectorizer.adapt(train_texts)
    
    X_train = vectorizer(train_texts)
    X_val = vectorizer(val_texts)
    X_test = vectorizer(test_texts)
    
    vocab_size = len(vectorizer.get_vocabulary())
    num_dept_classes = len(dept_encoder.classes_)
    num_severity_classes = len(severity_encoder.classes_)
    
    model = create_model(num_dept_classes, num_severity_classes, vocab_size, 100)
    model.summary()
    
    history = model.fit(
        X_train, {'department_output': train_dept, 'severity_output': train_sev},
        validation_data=(X_val, {'department_output': val_dept, 'severity_output': val_sev}),
        epochs=5, batch_size=32
    )
    
    # Evaluate
    results = model.evaluate(X_test, {'department_output': test_dept, 'severity_output': test_sev})
    print("Test Results:", dict(zip(model.metrics_names, results)))
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)
    
    model.save(os.path.join(model_dir, "grievance_model.keras"))
    
    # Save configs
    config = {
        "department_classes": list(dept_encoder.classes_),
        "severity_classes": list(severity_encoder.classes_)
    }
    
    with open(os.path.join(model_dir, "label_encoders.json"), 'w') as f:
        json.dump(config, f)
    
    vectorizer_config = {
        "max_tokens": 10000,
        "output_sequence_length": 100,
        "vocabulary": vectorizer.get_vocabulary()
    }
    
    with open(os.path.join(model_dir, "vectorizer_config.json"), 'w') as f:
        json.dump(vectorizer_config, f)
    
    print("Model training complete!")

if __name__ == "__main__":
    main()
