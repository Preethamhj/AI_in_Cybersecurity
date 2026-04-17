# ============================================
# WEEK 1: DATA PREPROCESSING & VISUALIZATION
# (UPGRADED VERSION)
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from mpl_toolkits.mplot3d import Axes3D


# ============================================
# LOAD DATASET
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
# CLEAN DATA
# ============================================

def clean_data(df):

    df = df.drop_duplicates()
    df = df.dropna()

    # Convert label to binary
    df['label'] = df['label'].apply(lambda x: 'Normal' if x == 'normal' else 'Attack')

    print("After Cleaning:", df.shape)

    return df


# ============================================
# ENCODE + SCALE (FOR FUTURE USE)
# ============================================

def encode_scale(df):

    df_encoded = df.copy()

    le = LabelEncoder()
    for col in ['protocol_type','service','flag']:
        df_encoded[col] = le.fit_transform(df_encoded[col])

    scaler = MinMaxScaler()
    num_cols = df_encoded.select_dtypes(include=np.number).columns
    df_encoded[num_cols] = scaler.fit_transform(df_encoded[num_cols])

    return df_encoded


# ============================================
# VISUALIZATION (RAW DATA ONLY)
# ============================================

def visualize(df):

    print("\nGenerating Visualizations...")

    # -------- 1. COUNT PLOT --------
    plt.figure(figsize=(6,4))
    sns.countplot(x='label', data=df)
    plt.title("Normal vs Attack Count")
    plt.show()


    # -------- 2. SCATTER (LOG SCALE) --------
    plt.figure(figsize=(6,4))
    plt.scatter(df['src_bytes'], df['dst_bytes'], alpha=0.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Scatter (Log Scale): src_bytes vs dst_bytes")
    plt.xlabel("src_bytes")
    plt.ylabel("dst_bytes")
    plt.show()


    # -------- 3. HEATMAP --------
    plt.figure(figsize=(12,8))
    numeric_df = df.select_dtypes(include=np.number)
    sns.heatmap(numeric_df.corr(), cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.show()


    # -------- 4. BOXPLOT --------
    plt.figure(figsize=(6,4))
    sns.boxplot(x='label', y='src_bytes', data=df)
    plt.yscale('log')
    plt.title("Boxplot (Log Scale): src_bytes vs Label")
    plt.show()


    # -------- 5. 3D SCATTER --------
    sample = df.sample(3000)

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(sample['src_bytes'], sample['dst_bytes'], sample['count'],
               alpha=0.5)

    ax.set_xlabel("src_bytes")
    ax.set_ylabel("dst_bytes")
    ax.set_zlabel("count")
    plt.title("3D Scatter Plot")
    plt.show()


    


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    # Load
    df = load_dataset("../datasets/KDDTrain+.txt")

    # Clean
    df = clean_data(df)

    # Keep RAW for visualization
    df_visual = df.copy()

    # Create scaled version (future weeks)
    df_scaled = encode_scale(df)

    # Visualize RAW data
    visualize(df_visual)

    print("\n✅ Week 1 Completed (Enhanced Visualization)")