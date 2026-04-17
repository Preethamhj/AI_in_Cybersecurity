# ============================================
# WEEK 2: PHISHING DETECTION (FIXED VERSION)
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt


# ============================================
# LOAD DATA
# ============================================

def load_data(filepath):
    df = pd.read_csv(filepath)
    print("Dataset Loaded:", df.shape)
    return df


# ============================================
# PREPROCESS DATA
# ============================================

def preprocess(df):

    print("\nColumns:")
    print(df.columns)

    # Target column (based on your dataset)
    target = 'phishing'

    # Features and labels
    X = df.drop(columns=[target])
    y = df[target]

    # Convert to numeric (just in case)
    X = X.apply(pd.to_numeric, errors='coerce')

    # Handle missing values
    X = X.fillna(0)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


# ============================================
# TRAIN MODELS
# ============================================

def train_models(X_train, y_train):

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(),
        "Naive Bayes": GaussianNB()
    }

    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model

    return trained_models


# ============================================
# EVALUATE MODELS
# ============================================

def evaluate(models, X_test, y_test):

    for name, model in models.items():

        print(f"\n===== {name} =====")

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        print("Accuracy:", acc)

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(4,3))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f"{name} Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    # Load dataset
    df = load_data("../datasets/dataset_full.csv")

    # Preprocess
    X, y = preprocess(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train models
    models = train_models(X_train, y_train)

    # Evaluate
    evaluate(models, X_test, y_test)

    print("\n✅ Week 2 Completed Successfully!")