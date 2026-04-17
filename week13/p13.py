# ============================================
# WEEK 13: EXPLAINABLE AI (SHAP)
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

import shap
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

    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)

    le = LabelEncoder()
    for col in ['protocol_type', 'service', 'flag']:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=['label', 'difficulty'])
    y = df['label']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


# ============================================
# TRAIN MODEL
# ============================================

def train_model(X_train, y_train):

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    return model


# ============================================
# SHAP EXPLANATION
# ============================================
def explain(model, X_sample, feature_names):

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X_sample)

    # Handle both formats
    if isinstance(shap_values, list):
        shap_values_to_use = shap_values[1]
    else:
        shap_values_to_use = shap_values

    # 🔥 1. Summary Plot (MOST IMPORTANT)
    shap.summary_plot(shap_values_to_use, X_sample, feature_names=feature_names)

    # 🔥 2. Feature Importance Bar Plot (VERY SAFE)
    shap.summary_plot(shap_values_to_use, X_sample,
                      feature_names=feature_names,
                      plot_type="bar")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y, feature_names = preprocess(df)

    # Use subset (important for SHAP speed)
    X = X[:2000]
    y = y[:2000]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = train_model(X_train, y_train)
    X_test = np.array(X_test)
    # Explain predictions
    explain(model, X_test[:100], feature_names)

    print("\n✅ Week 13 Completed Successfully!")