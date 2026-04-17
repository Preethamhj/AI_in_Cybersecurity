# ============================================
# WEEK 10: PCAP / BINETFLOW ANALYSIS
# ============================================

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


# ============================================
# LOAD DATA
# ============================================

def load_data(filepath):

    df = pd.read_csv(filepath)

    print("Dataset Loaded:", df.shape)
    print("\nColumns:\n", df.columns)

    return df


# ============================================
# PREPROCESS
# ============================================

def preprocess(df):

    # Drop non-useful columns if present
    drop_cols = ['StartTime', 'SrcAddr', 'DstAddr']
    for col in drop_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    # Handle categorical columns
    df = df.apply(LabelEncoder().fit_transform)

    # Separate features
    X = df.values

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled


# ============================================
# CLUSTERING (BOTNET DETECTION)
# ============================================

def detect_botnet(X):

    kmeans = KMeans(n_clusters=2, random_state=42)
    labels = kmeans.fit_predict(X)

    print("\nClustering Done!")

    return labels


# ============================================
# VISUALIZE
# ============================================

def visualize(X, labels):

    plt.figure(figsize=(10,6))

    unique_labels = np.unique(labels)

    for label in unique_labels:

        cluster_points = X[labels == label]

        # Assign meaningful names
        if label == 0:
            name = "Normal Traffic"
        else:
            name = "Suspicious / Botnet"

        plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                    label=name,
                    alpha=0.5,
                    s=10)

    plt.title("Botnet Detection (Clustering)")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")

    # Move legend outside (important)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_data("../datasets/capture20110810.binetflow")

    X = preprocess(df)

    # Use subset (important)
    X = X[:5000]

    labels = detect_botnet(X)

    visualize(X, labels)

    print("\n✅ Week 10 Completed Successfully!")