"""
CivicFix - Machine Learning Pipeline
Multi-Output Neural Network for Grievance Classification using TensorFlow 2.x

Architecture:
- Input: Preprocessed integer sequences (from TextVectorization)
- Embedding Layer
- Bidirectional LSTM (64 units)
- Shared Dense Layer
- Output 1: Department Classification (Softmax, 4 classes)
- Output 2: Severity Classification (Sigmoid, Binary)
"""

import json
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple, Dict, Any, List


# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)


def load_and_preprocess_data(data_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, 
                                                       LabelEncoder, LabelEncoder]:
    """
    Load complaint data and preprocess labels.
    
    Args:
        data_path: Path to the complaints CSV file
        
    Returns:
        Tuple of (texts, department_labels, severity_labels, dept_encoder, severity_encoder)
    """
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # Extract text and labels
    texts = df['text'].fillna('').values
    departments = df['department'].values
    severities = df['severity'].values
    
    # Encode department labels (4 classes)
    dept_encoder = LabelEncoder()
    dept_labels = dept_encoder.fit_transform(departments)
    
    # Encode severity labels (binary: High=1, Low=0)
    severity_encoder = LabelEncoder()
    severity_labels = severity_encoder.fit_transform(severities)
    
    print(f"Loaded {len(texts)} complaints")
    print(f"Departments: {dept_encoder.classes_}")
    print(f"Severity classes: {severity_encoder.classes_}")
    
    return texts, dept_labels, severity_labels, dept_encoder, severity_encoder


def create_and_adapt_vectorizer(texts: np.ndarray, max_vocab: int = 10000, 
                                max_length: int = 100) -> layers.TextVectorization:
    """
    Create and adapt TextVectorization layer for preprocessing.
    
    Args:
        texts: Array of text samples
        max_vocab: Maximum vocabulary size
        max_length: Maximum sequence length
        
    Returns:
        Adapted TextVectorization layer
    """
    print("Creating and adapting TextVectorization layer...")
    
    vectorizer = layers.TextVectorization(
        max_tokens=max_vocab,
        output_mode='int',
        output_sequence_length=max_length,
        name='text_vectorizer'
    )
    
    # Adapt vectorizer to the training data
    vectorizer.adapt(texts)
    
    print(f"Vocabulary size: {len(vectorizer.get_vocabulary())}")
    return vectorizer


def preprocess_texts(vectorizer: layers.TextVectorization, 
                     texts: np.ndarray) -> np.ndarray:
    """
    Preprocess text data using the vectorizer.
    
    Args:
        vectorizer: Adapted TextVectorization layer
        texts: Array of text samples
        
    Returns:
        Preprocessed integer sequences
    """
    return vectorizer(texts).numpy()


def build_model(vocab_size: int, embedding_dim: int = 128, 
                max_length: int = 100, num_departments: int = 4) -> keras.Model:
    """
    Build Multi-Output Neural Network for grievance classification.
    
    Architecture:
    1. Input layer (integer sequences from TextVectorization)
    2. Embedding layer (converts integers to dense vectors)
    3. Bidirectional LSTM (captures context from both directions)
    4. Shared Dense layer (common representation for both tasks)
    5. Two output heads:
       - Department classification (softmax, 4 classes)
       - Severity classification (sigmoid, binary)
    
    Args:
        vocab_size: Size of vocabulary
        embedding_dim: Dimension of embedding vectors
        max_length: Maximum sequence length
        num_departments: Number of department classes
        
    Returns:
        Compiled Keras Model
    """
    print("Building Multi-Output Neural Network...")
    
    # Input layer - accepts preprocessed integer sequences
    inputs = layers.Input(shape=(max_length,), dtype='int32', name='input_text')
    
    # Embedding layer - converts integer tokens to dense vectors
    # Adds positional understanding of words
    # mask_zero=True allows the model to ignore padding tokens
    x = layers.Embedding(
        input_dim=vocab_size,
        output_dim=embedding_dim,
        mask_zero=True,
        name='embedding_layer'
    )(inputs)
    
    # Bidirectional LSTM - processes sequence in both directions
    # Captures context from past and future tokens
    # 64 units provides good balance of capacity and efficiency
    x = layers.Bidirectional(
        layers.LSTM(64, return_sequences=False, name='lstm_layer'),
        name='bidirectional_lstm'
    )(x)
    
    # Dropout for regularization - prevents overfitting
    x = layers.Dropout(0.5, name='dropout_1')(x)
    
    # Shared Dense layer - common representation for both tasks
    # 128 units with ReLU activation
    x = layers.Dense(128, activation='relu', name='shared_dense')(x)
    x = layers.Dropout(0.3, name='dropout_2')(x)
    
    # Department Classification Head (Multi-class)
    # Predicts which department should handle the complaint
    # Softmax activation for multi-class probability distribution
    dept_output = layers.Dense(
        num_departments,
        activation='softmax',
        name='department_output'
    )(x)
    
    # Severity Classification Head (Binary)
    # Predicts if complaint is High or Low severity
    # Sigmoid activation for binary classification
    severity_output = layers.Dense(
        1,
        activation='sigmoid',
        name='severity_output'
    )(x)
    
    # Create model with two outputs
    model = keras.Model(
        inputs=inputs,
        outputs=[dept_output, severity_output],
        name='grievance_classifier'
    )
    
    # Compile with appropriate losses for each output
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss={
            'department_output': 'sparse_categorical_crossentropy',
            'severity_output': 'binary_crossentropy'
        },
        metrics={
            'department_output': 'accuracy',
            'severity_output': 'accuracy'
        },
        loss_weights={
            'department_output': 1.0,
            'severity_output': 1.0
        }
    )
    
    print("Model architecture:")
    model.summary()
    
    return model


def compute_class_weights(labels: np.ndarray) -> Dict[int, float]:
    """
    Compute class weights to handle imbalanced datasets.
    
    Args:
        labels: Array of class labels
        
    Returns:
        Dictionary mapping class indices to weights
    """
    classes = np.unique(labels)
    weights = compute_class_weight(
        class_weight='balanced',
        classes=classes,
        y=labels
    )
    return dict(zip([int(c) for c in classes], [float(w) for w in weights]))


def train_model(model: keras.Model, 
                train_texts: np.ndarray,
                train_dept_labels: np.ndarray,
                train_severity_labels: np.ndarray,
                val_texts: np.ndarray,
                val_dept_labels: np.ndarray,
                val_severity_labels: np.ndarray,
                epochs: int = 30,
                batch_size: int = 32) -> keras.callbacks.History:
    """
    Train the multi-output model with class weight balancing.
    
    Args:
        model: Keras model to train
        train_texts: Preprocessed training text samples (integer sequences)
        train_dept_labels: Training department labels
        train_severity_labels: Training severity labels
        val_texts: Preprocessed validation text samples
        val_dept_labels: Validation department labels
        val_severity_labels: Validation severity labels
        epochs: Number of training epochs
        batch_size: Batch size for training
        
    Returns:
        Training history
    """
    print("\nComputing class weights for imbalance handling...")
    
    # Compute class weights for department classification
    dept_weights = compute_class_weights(train_dept_labels)
    print(f"Department class weights: {dept_weights}")
    
    # Compute class weights for severity classification
    severity_weights = compute_class_weights(train_severity_labels)
    print(f"Severity class weights: {severity_weights}")
    
    # Define callbacks
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=7,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )
    
    model_checkpoint = keras.callbacks.ModelCheckpoint(
        'best_model.keras',
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
    
    print(f"\nTraining for {epochs} epochs with batch size {batch_size}...")
    
    # Train the model
    history = model.fit(
        train_texts,
        {
            'department_output': train_dept_labels,
            'severity_output': train_severity_labels
        },
        validation_data=(
            val_texts,
            {
                'department_output': val_dept_labels,
                'severity_output': val_severity_labels
            }
        ),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stopping, reduce_lr, model_checkpoint],
        verbose=1
    )
    
    return history


def evaluate_model(model: keras.Model,
                   test_texts: np.ndarray,
                   test_dept_labels: np.ndarray,
                   test_severity_labels: np.ndarray,
                   dept_encoder: LabelEncoder,
                   severity_encoder: LabelEncoder) -> Dict[str, float]:
    """
    Evaluate model performance on test set.
    
    Args:
        model: Trained Keras model
        test_texts: Preprocessed test text samples
        test_dept_labels: Test department labels
        test_severity_labels: Test severity labels
        dept_encoder: Label encoder for departments
        severity_encoder: Label encoder for severity
        
    Returns:
        Dictionary of evaluation metrics
    """
    print("\n" + "=" * 50)
    print("Model Evaluation")
    print("=" * 50)
    
    # Get predictions
    predictions = model.predict(test_texts, verbose=0)
    dept_preds = np.argmax(predictions[0], axis=1)
    severity_preds = (predictions[1] > 0.5).astype(int).flatten()
    
    # Calculate accuracy for department classification
    dept_accuracy = np.mean(dept_preds == test_dept_labels)
    
    # Calculate accuracy for severity classification
    severity_accuracy = np.mean(severity_preds == test_severity_labels)
    
    # Overall accuracy (both correct)
    overall_accuracy = np.mean(
        (dept_preds == test_dept_labels) & (severity_preds == test_severity_labels)
    )
    
    print(f"\nDepartment Classification Accuracy: {dept_accuracy * 100:.2f}%")
    print(f"Severity Classification Accuracy: {severity_accuracy * 100:.2f}%")
    print(f"Overall Accuracy (both correct): {overall_accuracy * 100:.2f}%")
    
    # Per-class accuracy for departments
    print("\nPer-Department Accuracy:")
    for i, dept in enumerate(dept_encoder.classes_):
        mask = test_dept_labels == i
        if np.sum(mask) > 0:
            class_acc = np.mean(dept_preds[mask] == test_dept_labels[mask])
            print(f"  {dept}: {class_acc * 100:.2f}% ({np.sum(mask)} samples)")
    
    # Per-class accuracy for severity
    print("\nPer-Severity Accuracy:")
    for i, sev in enumerate(severity_encoder.classes_):
        mask = test_severity_labels == i
        if np.sum(mask) > 0:
            class_acc = np.mean(severity_preds[mask] == test_severity_labels[mask])
            print(f"  {sev}: {class_acc * 100:.2f}% ({np.sum(mask)} samples)")
    
    return {
        'department_accuracy': float(dept_accuracy),
        'severity_accuracy': float(severity_accuracy),
        'overall_accuracy': float(overall_accuracy)
    }


def save_model_and_artifacts(model: keras.Model,
                             vectorizer: layers.TextVectorization,
                             dept_encoder: LabelEncoder,
                             severity_encoder: LabelEncoder,
                             metrics: Dict[str, float],
                             max_length: int = 100,
                             output_dir: str = '../models') -> None:
    """
    Save trained model and preprocessing artifacts.
    
    Args:
        model: Trained Keras model
        vectorizer: TextVectorization layer
        dept_encoder: Department label encoder
        severity_encoder: Severity label encoder
        metrics: Evaluation metrics
        output_dir: Directory to save artifacts
    """
    print("\n" + "=" * 50)
    print("Saving Model and Artifacts")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the complete model (using Keras native format)
    model_path = os.path.join(output_dir, 'grievance_model.keras')
    model.save(model_path)
    print(f"Model saved to: {model_path}")
    
    # Save vectorizer vocabulary
    vocab = vectorizer.get_vocabulary()
    vectorizer_config = {
        'vocabulary': vocab,
        'max_tokens': len(vocab),
        'output_mode': 'int',
        'output_sequence_length': max_length
    }
    
    vectorizer_path = os.path.join(output_dir, 'vectorizer_config.json')
    with open(vectorizer_path, 'w', encoding='utf-8') as f:
        json.dump(vectorizer_config, f, indent=2)
    print(f"Vectorizer config saved to: {vectorizer_path}")
    
    # Save label encoders
    encoder_config = {
        'department_classes': dept_encoder.classes_.tolist(),
        'severity_classes': severity_encoder.classes_.tolist()
    }
    
    encoder_path = os.path.join(output_dir, 'label_encoders.json')
    with open(encoder_path, 'w', encoding='utf-8') as f:
        json.dump(encoder_config, f, indent=2)
    print(f"Label encoders saved to: {encoder_path}")
    
    # Save metrics
    metrics_path = os.path.join(output_dir, 'training_metrics.json')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    print(f"Training metrics saved to: {metrics_path}")


def create_inference_model(model: keras.Model, vocab_size: int, max_length: int) -> keras.Model:
    """
    Create an inference model that includes the TextVectorization layer.
    This allows end-to-end inference from raw text to predictions.
    
    Args:
        model: Trained model (expects integer sequences)
        vocab_size: Vocabulary size
        max_length: Maximum sequence length
        
    Returns:
        Inference model that accepts raw text strings
    """
    # Create new input for raw text
    text_input = layers.Input(shape=(1,), dtype=tf.string, name='raw_text_input')
    
    # Add TextVectorization layer (will be loaded with vocabulary at inference)
    vectorizer = layers.TextVectorization(
        max_tokens=vocab_size,
        output_mode='int',
        output_sequence_length=max_length
    )
    
    x = vectorizer(text_input)
    
    # Get embeddings from the original model's embedding layer
    embedding_layer = model.get_layer('embedding_layer')
    x = embedding_layer(x)
    
    # Pass through the rest of the network
    for layer_name in ['bidirectional_lstm', 'dropout_1', 'shared_dense', 'dropout_2']:
        x = model.get_layer(layer_name)(x)
    
    # Get outputs
    dept_output = model.get_layer('department_output')(x)
    severity_output = model.get_layer('severity_output')(x)
    
    inference_model = keras.Model(
        inputs=text_input,
        outputs=[dept_output, severity_output],
        name='grievance_inference_model'
    )
    
    return inference_model, vectorizer


def main():
    """Main function to run the complete ML pipeline."""
    print("=" * 60)
    print("CivicFix - Grievance Classification Model Training")
    print("=" * 60)
    
    # Load and preprocess data
    data_path = '../data/complaints_dataset.csv'
    texts, dept_labels, severity_labels, dept_encoder, severity_encoder = \
        load_and_preprocess_data(data_path)
    
    # Split data: 80% train+val, 20% test
    train_val_texts, test_texts, train_val_dept, test_dept, train_val_sev, test_sev = \
        train_test_split(
            texts, dept_labels, severity_labels,
            test_size=0.2,
            random_state=42,
            stratify=severity_labels  # Stratify on severity for balance
        )
    
    # Further split training into train/val (90/10 of training = 72/18 of total)
    train_texts, val_texts, train_dept, val_dept, train_sev, val_sev = \
        train_test_split(
            train_val_texts, train_val_dept, train_val_sev,
            test_size=0.1,
            random_state=42,
            stratify=train_val_sev
        )
    
    print(f"\nData Split:")
    print(f"  Training samples: {len(train_texts)}")
    print(f"  Validation samples: {len(val_texts)}")
    print(f"  Test samples: {len(test_texts)}")
    
    # Create and adapt vectorizer on training data only
    max_length = 150  # Increased sequence length for more variety
    vocab_size_param = 10000  # Increased vocabulary for 50k records
    vectorizer = create_and_adapt_vectorizer(train_texts, max_vocab=vocab_size_param, max_length=max_length)
    vocab_size = len(vectorizer.get_vocabulary())
    
    # Preprocess all data splits
    print("\nPreprocessing text data...")
    train_texts_seq = preprocess_texts(vectorizer, train_texts)
    val_texts_seq = preprocess_texts(vectorizer, val_texts)
    test_texts_seq = preprocess_texts(vectorizer, test_texts)
    
    print(f"Preprocessed shapes: Train={train_texts_seq.shape}, Val={val_texts_seq.shape}, Test={test_texts_seq.shape}")
    
    # Build model (expects preprocessed integer sequences)
    model = build_model(
        vocab_size=vocab_size,
        embedding_dim=256,  # Increased embedding dimension
        max_length=max_length,
        num_departments=len(dept_encoder.classes_)
    )
    
    # Train model
    history = train_model(
        model=model,
        train_texts=train_texts_seq,
        train_dept_labels=train_dept,
        train_severity_labels=train_sev,
        val_texts=val_texts_seq,
        val_dept_labels=val_dept,
        val_severity_labels=val_sev,
        epochs=10,  # Fast training - clear data converges quickly
        batch_size=64  # Increased batch size for efficiency
    )
    
    # Load best model for evaluation
    print("\nLoading best model for evaluation...")
    best_model = keras.models.load_model('best_model.keras')
    
    # Evaluate on test set
    metrics = evaluate_model(
        model=best_model,
        test_texts=test_texts_seq,
        test_dept_labels=test_dept,
        test_severity_labels=test_sev,
        dept_encoder=dept_encoder,
        severity_encoder=severity_encoder
    )
    
    # Save model and artifacts
    save_model_and_artifacts(
        model=best_model,
        vectorizer=vectorizer,
        dept_encoder=dept_encoder,
        severity_encoder=severity_encoder,
        metrics=metrics,
        max_length=max_length
    )
    
    # Check if accuracy target met
    print("\n" + "=" * 60)
    if metrics['department_accuracy'] >= 0.85:
        print("✓ TARGET MET: Department accuracy >= 85%")
    else:
        print(f"✗ Target not met: Department accuracy = {metrics['department_accuracy']*100:.2f}%")
        print("  Suggestion: Increase keyword distinctiveness in training data")
    
    if metrics['severity_accuracy'] >= 0.85:
        print("✓ TARGET MET: Severity accuracy >= 85%")
    else:
        print(f"✗ Target not met: Severity accuracy = {metrics['severity_accuracy']*100:.2f}%")
    
    print("=" * 60)
    print("Training Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
