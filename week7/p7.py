# ============================================
# WEEK 7: DIMENSIONALITY REDUCTION (PCA)
# ============================================

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA

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

    # Convert label for visualization
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

    # Encode categorical features
    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    # Features & labels
    X = df.drop(columns=['label', 'difficulty'])
    y = df['label']

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


# ============================================
# APPLY PCA
# ============================================

def apply_pca(X):

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    print("Explained Variance:", pca.explained_variance_ratio_)

    return X_pca


# ============================================
# VISUALIZE
# ============================================

def visualize(X_pca, y):

    plt.figure(figsize=(8,6))

    # Normal
    plt.scatter(X_pca[y == 0, 0],
                X_pca[y == 0, 1],
                label="Normal",
                alpha=0.5)

    # Attack
    plt.scatter(X_pca[y == 1, 0],
                X_pca[y == 1, 1],
                label="Attack",
                alpha=0.5)

    plt.title("PCA: Malware Behavior Visualization")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")

    plt.legend()
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y = preprocess(df)

    # Use subset for faster visualization
    X = X[:80000]
    y = y[:80000]

    X_pca = apply_pca(X)

    visualize(X_pca, y)

    print("\n✅ Week 7 Completed Successfully!")