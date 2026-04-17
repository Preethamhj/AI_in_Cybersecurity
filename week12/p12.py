# ============================================
# WEEK 12: HYBRID IDS (SUPERVISED + UNSUPERVISED)
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest

from sklearn.metrics import accuracy_score


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

    X = df.drop(columns=['label', 'difficulty'])
    y = df['label']

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y


# ============================================
# SUPERVISED MODEL
# ============================================

def train_supervised(X_train, y_train):

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    return model


# ============================================
# UNSUPERVISED MODEL
# ============================================

def train_unsupervised(X_train):

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X_train)

    return model


# ============================================
# HYBRID DETECTION
# ============================================

def hybrid_detection(supervised_model, unsupervised_model, X_test):

    # Supervised prediction
    y_super = supervised_model.predict(X_test)

    # Unsupervised prediction (-1 anomaly, 1 normal)
    y_unsuper = unsupervised_model.predict(X_test)

    # Convert to 0/1
    y_unsuper = np.where(y_unsuper == -1, 1, 0)

    # Hybrid: if either detects attack → attack
    y_final = np.where((y_super == 1) | (y_unsuper == 1), 1, 0)

    return y_super, y_unsuper, y_final


# ============================================
# EVALUATION
# ============================================

def evaluate(y_test, y_super, y_unsuper, y_final):

    print("\nSupervised Accuracy:", accuracy_score(y_test, y_super))
    print("Unsupervised Approx Accuracy:", accuracy_score(y_test, y_unsuper))
    print("Hybrid Accuracy:", accuracy_score(y_test, y_final))


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_dataset("../datasets/KDDTrain+.txt")

    X, y = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train models
    supervised_model = train_supervised(X_train, y_train)
    unsupervised_model = train_unsupervised(X_train)

    # Hybrid prediction
    y_super, y_unsuper, y_final = hybrid_detection(
        supervised_model, unsupervised_model, X_test
    )

    # Evaluate
    evaluate(y_test, y_super, y_unsuper, y_final)

    print("\n✅ Week 12 Completed Successfully!")