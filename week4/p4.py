# ============================================
# WEEK 4: INTRUSION DETECTION SYSTEM (IDS)
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

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

    # Encode categorical features
    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    # Features & Target
    X = df.drop(columns=['label', 'difficulty'])
    y = df['label']

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


# ============================================
# TRAIN MODEL
# ============================================

def train_model(X_train, y_train):

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    return model


# ============================================
# EVALUATE
# ============================================

def evaluate(model, X_test, y_test):

    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(4,3))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)

    evaluate(model, X_test, y_test)

    print("\n✅ Week 4 Completed Successfully!")