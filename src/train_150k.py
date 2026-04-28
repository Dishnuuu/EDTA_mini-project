"""
CivicFix - ML Training Pipeline with 150k data
Multi-Output Neural Network for Grievance Classification
"""

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

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "complaints_150k_final.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

def load_and_preprocess_data(data_path):
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    df = df.dropna(subset=['Complaint_Text', 'Category', 'Severity'])
    df = df[df['Category'].isin(['Electricity', 'Water Supply', 'Waste-Water/Sewage'])]
    df = df[df['Severity'].isin(['High', 'Low'])]
    
    texts = df['Complaint_Text'].fillna('').values
    departments = df['Category'].values
    severities = df['Severity'].values
    
    dept_encoder = LabelEncoder()
    dept_labels = dept_encoder.fit_transform(departments)
    
    severity_encoder = LabelEncoder()
    severity_labels = severity_encoder.fit_transform(severities)
    
    print(f"Loaded {len(texts)} complaints")
    print(f"Department classes: {dept_encoder.classes_}")
    print(f"Severity classes: {severity_encoder.classes_}")
    
    return texts, dept_labels, severity_labels, dept_encoder, severity_encoder

def create_model(num_dept_classes, num_severity_classes, vocab_size, max_length):
    inputs = keras.Input(shape=(max_length,))
    x = layers.Embedding(vocab_size, 128)(inputs)
    x = layers.Bidirectional(layers.LSTM(64))(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    
    # Use softmax for both outputs to match label shapes
    dept_output = layers.Dense(num_dept_classes, activation='softmax', name='department_output')(x)
    severity_output = layers.Dense(num_severity_classes, activation='softmax', name='severity_output')(x)
    
    model = keras.Model(inputs=inputs, outputs=[dept_output, severity_output])
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss={
            'department_output': 'sparse_categorical_crossentropy',
            'severity_output': 'sparse_categorical_crossentropy'
        },
        metrics={
            'department_output': 'accuracy',
            'severity_output': 'accuracy'
        }
    )
    return model

def main():
    print("="*60)
    print("CivicFit - ML Training with 150k data")
    print("="*60)
    
    texts, dept_labels, severity_labels, dept_encoder, severity_encoder = load_and_preprocess_data(DATA_PATH)
    
    # Split data
    train_val_texts, test_texts, train_val_dept, test_dept, train_val_sev, test_sev = train_test_split(
        texts, dept_labels, severity_labels,
        test_size=0.2, random_state=42, stratify=severity_labels
    )
    
    train_texts, val_texts, train_dept, val_dept, train_sev, val_sev = train_test_split(
        train_val_texts, train_val_dept, train_val_sev,
        test_size=0.1, random_state=42
    )
    
    print(f"Training set: {len(train_texts)}")
    print(f"Validation set: {len(val_texts)}")
    print(f"Test set: {len(test_texts)}")
    
    # Vectorize
    print("\nVectorizing text...")
    vectorizer = layers.TextVectorization(max_tokens=15000, output_mode='int', output_sequence_length=100)
    vectorizer.adapt(train_texts)
    
    X_train = vectorizer(train_texts)
    X_val = vectorizer(val_texts)
    X_test = vectorizer(test_texts)
    
    vocab_size = len(vectorizer.get_vocabulary())
    num_dept_classes = len(dept_encoder.classes_)
    num_severity_classes = len(severity_encoder.classes_)
    
    print(f"Vocabulary size: {vocab_size}")
    print(f"Department classes: {num_dept_classes}")
    print(f"Severity classes: {num_severity_classes}")
    
    # Create and train model
    print("\nCreating model...")
    model = create_model(num_dept_classes, num_severity_classes, vocab_size, 100)
    model.summary()
    
    print("\nTraining model...")
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=3, restore_best_weights=True
    )
    
    history = model.fit(
        X_train, {'department_output': train_dept, 'severity_output': train_sev},
        validation_data=(X_val, {'department_output': val_dept, 'severity_output': val_sev}),
        epochs=10, batch_size=64, callbacks=[early_stop], verbose=1
    )
    
    # Evaluate
    print("\nEvaluating model...")
    results = model.evaluate(X_test, {'department_output': test_dept, 'severity_output': test_sev}, verbose=0)
    print(f"Test Department Accuracy: {results[3]:.4f}")
    print(f"Test Severity Accuracy: {results[4]:.4f}")
    print(f"Test Total Loss: {results[0]:.4f}")
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, "grievance_model.keras")
    model.save(model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Save configs
    config = {
        "department_classes": list(dept_encoder.classes_),
        "severity_classes": list(severity_encoder.classes_)
    }
    
    config_path = os.path.join(MODEL_DIR, "label_encoders.json")
    with open(config_path, 'w') as f:
        json.dump(config, f)
    print(f"Config saved to: {config_path}")
    
    vectorizer_config = {
        "max_tokens": 15000,
        "output_sequence_length": 100,
        "vocabulary": vectorizer.get_vocabulary()
    }
    
    vec_path = os.path.join(MODEL_DIR, "vectorizer_config.json")
    with open(vec_path, 'w') as f:
        json.dump(vectorizer_config, f)
    print(f"Vectorizer config saved to: {vec_path}")
    
    print("\n" + "="*60)
    print("ML Training Complete!")
    print("="*60)

if __name__ == "__main__":
    main()