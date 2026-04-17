# ============================================
# WEEK 5: CLUSTERING (K-MEANS + DBSCAN)
# ============================================

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans, DBSCAN

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

    # Encode categorical features
    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    # Drop label (unsupervised)
    X = df.drop(columns=['label', 'difficulty'])

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled


# ============================================
# K-MEANS
# ============================================

def apply_kmeans(X):

    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(X)

    print("\nK-Means Clustering Done!")
    return labels


# ============================================
# DBSCAN
# ============================================

def apply_dbscan(X):

    dbscan = DBSCAN(eps=2, min_samples=10)
    labels = dbscan.fit_predict(X)

    print("\nDBSCAN Clustering Done!")
    return labels


# ============================================
# VISUALIZATION
# ============================================
def visualize(X, labels, title):

    plt.figure(figsize=(10,6))  # bigger figure

    unique_labels = np.unique(labels)
    max_clusters = 5
    shown_labels = unique_labels[:max_clusters]

    for label in shown_labels:

        cluster_points = X[labels == label]

        # Noise handling
        if label == -1:
            plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                        label='Noise (Anomaly)',
                        alpha=0.6, s=10)
        else:
            plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                        label=f'Cluster {label}',
                        alpha=0.6, s=10)

    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")

    # 🔥 Move legend outside
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout so graph doesn't shrink
    plt.tight_layout()

    plt.show()
# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X = preprocess(df)
    X_sample = X[:10000]   # or 3000 if needed

    # K-Means
    kmeans_labels = apply_kmeans(X)
    visualize(X, kmeans_labels, "K-Means Clustering")

    # DBSCAN
    dbscan_labels = apply_dbscan(X_sample)
    visualize(X_sample, dbscan_labels, "DBSCAN Clustering")

    print("\n✅ Week 5 Completed Successfully!")