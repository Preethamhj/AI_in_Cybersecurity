# ============================================
# WEEK 8: PHISHING URL DETECTION
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

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
# PREPROCESS
# ============================================

def preprocess(df):

    target = 'phishing'

    X = df.drop(columns=[target])
    y = df[target]

    # Convert to numeric
    X = X.apply(pd.to_numeric, errors='coerce')
    X = X.fillna(0)

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


# ============================================
# TRAIN MODELS
# ============================================

def train_models(X_train, y_train):

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100)
    }

    trained = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        trained[name] = model

    return trained


# ============================================
# EVALUATE
# ============================================

def evaluate(models, X_test, y_test):

    for name, model in models.items():

        print(f"\n===== {name} =====")

        y_pred = model.predict(X_test)

        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("\nReport:\n", classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(4,3))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f"{name} Confusion Matrix")
        plt.show()


# ============================================
# FEATURE IMPORTANCE
# ============================================

def feature_importance(model, feature_names):

    importances = model.feature_importances_

    # Top 10 features
    indices = np.argsort(importances)[-10:]

    plt.figure(figsize=(8,5))
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.title("Top 10 Important URL Features")
    plt.xlabel("Importance")
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_data("../datasets/dataset_full.csv")

    X, y, feature_names = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = train_models(X_train, y_train)

    evaluate(models, X_test, y_test)

    # Feature importance (Random Forest)
    feature_importance(models["Random Forest"], feature_names)

    print("\n✅ Week 8 Completed Successfully!")