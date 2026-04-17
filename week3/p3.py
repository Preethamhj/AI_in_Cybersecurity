# ============================================
# WEEK 3: ANOMALY DETECTION (UNSUPERVISED)
# ============================================

import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler

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

    # Convert label for evaluation only
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

    # Encode categorical features
    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    # Drop label for UNSUPERVISED learning
    X = df.drop(columns=['label', 'difficulty'])

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, df['label']


# ============================================
# ANOMALY DETECTION
# ============================================

def detect_anomalies(X):

    # Isolation Forest model
    model = IsolationForest(contamination=0.1, random_state=42)

    model.fit(X)

    predictions = model.predict(X)   # 1 (normal), -1 (anomaly)

    return predictions


# ============================================
# EVALUATION
# ============================================

def evaluate(predictions, true_labels):

    # Convert predictions:
    # -1 → anomaly → 1
    # 1 → normal → 0
    pred = np.where(predictions == -1, 1, 0)

    print("\nDetected Anomalies:", np.sum(pred))

    # Compare with true labels
    accuracy = np.mean(pred == true_labels)
    print("Approx Accuracy:", accuracy)


# ============================================
# VISUALIZATION
# ============================================
def visualize(X, predictions):

    # Convert predictions
    normal = X[predictions == 1]
    anomaly = X[predictions == -1]

    plt.figure(figsize=(6,4))

    # Plot normal points
    plt.scatter(normal[:, 0], normal[:, 1],
                color='blue', label='Normal', alpha=0.5)

    # Plot anomalies
    plt.scatter(anomaly[:, 0], anomaly[:, 1],
                color='red', label='Anomaly', alpha=0.5)

    plt.title("Anomaly Detection Visualization")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")

    plt.legend()
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y = preprocess(df)

    predictions = detect_anomalies(X)

    evaluate(predictions, y)

    visualize(X, predictions)

    print("\n✅ Week 3 Completed Successfully!")