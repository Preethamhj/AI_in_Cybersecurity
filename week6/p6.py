# ============================================
# WEEK 6: MALWARE CLASSIFICATION
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import seaborn as sns
import matplotlib.pyplot as plt


# ============================================
# LOAD DATA
# ============================================

def load_dataset(filepath):

    columns = [
        'duration','protocol_type','service','flag','src_bytes','dst_bytes',
        'land','wrong_fragment','urgent','hot','num_failed_logins','logged_in',
        'num_compromised','root_shell','su_attempted','num_root','num_file_creations',
        'num_shells','num_access_files','num_outbound_cmds','is_host_login',
        'is_guest_login','count','srv_count','serror_rate','srv_serror_rate',
        'rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate',
        'srv_diff_host_rate','dst_host_count','dst_host_srv_count',
        'dst_host_same_srv_rate','dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate','dst_host_srv_diff_host_rate',
        'dst_host_serror_rate','dst_host_srv_serror_rate',
        'dst_host_rerror_rate','dst_host_srv_rerror_rate','label','difficulty'
    ]

    df = pd.read_csv(filepath, names=columns)
    print("Dataset Loaded:", df.shape)

    return df


# ============================================
# PREPROCESS
# ============================================

def preprocess(df):

    # Convert label
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

    # Encode categorical
    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    # Split features & target
    X = df.drop(columns=['label', 'difficulty'])
    y = df['label']

    # Scale features (important for SVM)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


# ============================================
# TRAIN MODELS
# ============================================

def train_models(X_train, y_train):

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100),
        "SVM": SVC()
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

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(4,3))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f"{name} Confusion Matrix")
        plt.show()


# ============================================
# FEATURE IMPORTANCE (KEY PART)
# ============================================

def feature_importance(model, feature_names):

    importances = model.feature_importances_

    # Sort top features
    indices = np.argsort(importances)[-10:]

    plt.figure(figsize=(8,5))
    plt.barh(range(len(indices)), importances[indices])
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.title("Top 10 Important Features")
    plt.xlabel("Importance")
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y, feature_names = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = train_models(X_train, y_train)

    evaluate(models, X_test, y_test)

    # Feature importance (only Random Forest)
    feature_importance(models["Random Forest"], feature_names)

    print("\n✅ Week 6 Completed Successfully!")