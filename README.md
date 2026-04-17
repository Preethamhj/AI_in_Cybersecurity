# AI in Cyber Security Laboratory

This repository contains 13 weekly lab programs for an `AI in Cyber Security` laboratory course. The implementation in this folder follows the topics listed in the lab document and organizes them as standalone Python scripts from `week1` to `week13`, along with the datasets required to run them.

The README is arranged in a professional order for easier usage:

1. Lab overview from the document
2. Datasets used in this repository
3. Week-wise explanation of each program
4. Installation and setup
5. Expected outputs

## Lab Programs From The Document

The following lab objectives are preserved from the provided document:

### Week 1
- Write a program to preprocess and visualize cyber threat datasets to understand attack patterns and data characteristics.

### Week 2
- Write a program to implement supervised classification for spam or phishing detection using algorithms such as:
  - Logistic Regression
  - Decision Trees
  - Naive Bayes

### Week 3
- Write a program to implement an anomaly detection system using unsupervised learning techniques for identifying network intrusions.

### Week 4
- Write a program to design and evaluate an Intrusion Detection System (IDS) using machine learning algorithms and performance metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-Score

### Week 5
- Write a program to apply clustering algorithms (K-Means, DBSCAN) for detecting abnormal patterns and grouping malicious network traffic.

### Week 6
- Write a program to implement malware classification using feature extraction and supervised learning models such as:
  - Random Forest
  - SVM

### Week 7
- Write a program to perform malware behavior analysis using unsupervised learning and dimensionality reduction techniques.

### Week 8
- Write a program to implement phishing URL detection using machine learning with:
  - Lexical features
  - Content-based features

### Week 9
- Write a program to simulate adversarial attacks on machine learning models and demonstrate model robustness evaluation.

### Week 10
- Write a program to analyze network traffic captures (PCAP files) and extract features for botnet detection using classification or clustering methods.

### Week 11
- Write a program to design a predictive model to detect brute-force or penetration attack attempts from log or network data.

### Week 12
- Write a program to build and test a hybrid intrusion detection system combining supervised and unsupervised approaches for adaptive security.

### Week 13
- Write a program to implement feature engineering and model explainability techniques (e.g., SHAP or LIME) for AI-driven cyber threat detection systems.

## Repository Structure

```text
msc-lab/
├── datasets/
│   ├── KDDTrain+.txt
│   ├── KDDTest+.txt
│   ├── dataset_full.csv
│   ├── capture20110810.binetflow
│   ├── auth.log
│   └── spam.csv
├── week1/   ─ p1.py
├── week2/   ─ p2.py
├── week3/   ─ p3.py
├── week4/   ─ p4.py
├── week5/   ─ p5.py
├── week6/   ─ p6.py
├── week7/   ─ p7.py
├── week8/   ─ p8.py
├── week9/   ─ p9.py
├── week10/  ─ p10.py
├── week11/  ─ p11.py
├── week12/  ─ p12.py
├── week13/  ─ p13.py
└── README.md
```

## Datasets Used

Only a short description is included here so the focus stays on the lab programs.

### 1. `datasets/KDDTrain+.txt` and `datasets/KDDTest+.txt`
- Based on the NSL-KDD intrusion detection dataset.
- Contains network connection records with normal and attack labels.
- Used heavily across the repository for preprocessing, anomaly detection, IDS, clustering, malware-style classification, behavior analysis, adversarial simulation, hybrid IDS, and explainability.

### 2. `datasets/dataset_full.csv`
- A phishing URL dataset with engineered URL-based features and a `phishing` target column.
- Used in Week 2 and Week 8 for supervised phishing detection.

### 3. `datasets/capture20110810.binetflow`
- A network flow capture derived from botnet traffic analysis data.
- Used in Week 10 for clustering-based suspicious traffic detection.

### 4. `datasets/auth.log`
- Authentication log file containing login activity and failed login attempts.
- Used in Week 11 to detect brute-force behavior by analyzing repeated failures from the same IP address.

### 5. `datasets/spam.csv`
- A spam-related dataset present in the repository.
- It is not currently used by the provided scripts, but it is relevant to the Week 2 lab theme mentioned in the document.

## Program-Wise Explanation

Each week below includes:
- the lab objective,
- the file used in this repository,
- the dataset involved,
- what the program actually does,
- and the output it generates.

### Week 1: Data Preprocessing and Visualization

**Lab objective**
- Preprocess and visualize cyber threat datasets to understand attack patterns and data characteristics.

**Program**
- `week1/p1.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads the NSL-KDD style dataset with explicit column names.
- Removes duplicate rows and missing values.
- Converts the class label into binary-style categories: `Normal` and `Attack`.
- Encodes categorical features such as `protocol_type`, `service`, and `flag`.
- Applies Min-Max scaling to numeric features.
- Produces multiple visualizations from the raw cleaned dataset.

**Techniques used**
- `pandas`, `numpy`
- `LabelEncoder`, `MinMaxScaler`
- `matplotlib`, `seaborn`

**Output**
- Dataset shape before and after cleaning.
- Count plot for normal vs attack classes.
- Scatter plot of `src_bytes` vs `dst_bytes` in log scale.
- Correlation heatmap for numeric features.
- Boxplot comparing `src_bytes` across labels.
- 3D scatter plot for selected traffic features.

### Week 2: Supervised Classification for Phishing Detection

**Lab objective**
- Implement supervised classification for spam or phishing detection using Logistic Regression, Decision Tree, and Naive Bayes.

**Program**
- `week2/p2.py`

**Dataset used**
- `datasets/dataset_full.csv`

**What the program does**
- Loads a phishing feature dataset.
- Uses the `phishing` column as the target label.
- Converts all features to numeric values and fills missing values with `0`.
- Scales the feature set using `StandardScaler`.
- Splits the data into training and testing sets.
- Trains three supervised models:
  - Logistic Regression
  - Decision Tree
  - Gaussian Naive Bayes
- Evaluates each model on test data.

**Techniques used**
- `train_test_split`
- `StandardScaler`
- `LogisticRegression`
- `DecisionTreeClassifier`
- `GaussianNB`

**Output**
- Dataset shape and column names.
- Accuracy score for each algorithm.
- Classification report for each algorithm.
- Confusion matrix heatmap for each model.

### Week 3: Anomaly Detection Using Unsupervised Learning

**Lab objective**
- Implement an anomaly detection system using unsupervised learning techniques for identifying network intrusions.

**Program**
- `week3/p3.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads the NSL-KDD dataset.
- Converts normal and attack labels into `0` and `1` only for approximate evaluation.
- Encodes categorical features and removes the `label` and `difficulty` columns from the training features.
- Scales the feature set.
- Trains an `IsolationForest` model to detect outliers.
- Converts anomaly predictions into binary output for interpretation.

**Techniques used**
- `IsolationForest`
- `LabelEncoder`
- `StandardScaler`

**Output**
- Number of anomalies detected.
- Approximate accuracy by comparing anomaly labels to the known target labels.
- Scatter plot showing normal points and anomaly points.

### Week 4: Intrusion Detection System (IDS)

**Lab objective**
- Design and evaluate an Intrusion Detection System using machine learning algorithms and metrics such as accuracy, precision, recall, and F1-score.

**Program**
- `week4/p4.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads the NSL-KDD dataset.
- Converts labels into binary classes: normal or attack.
- Encodes categorical fields and scales the features.
- Splits data into training and testing sets.
- Trains a `DecisionTreeClassifier`.
- Evaluates the trained model using common IDS performance metrics.

**Techniques used**
- `DecisionTreeClassifier`
- `accuracy_score`
- `precision_score`
- `recall_score`
- `f1_score`

**Output**
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix heatmap

### Week 5: Clustering with K-Means and DBSCAN

**Lab objective**
- Apply clustering algorithms for detecting abnormal patterns and grouping malicious network traffic.

**Program**
- `week5/p5.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads the NSL-KDD dataset.
- Encodes categorical features.
- Removes label information to perform unsupervised analysis.
- Scales the data.
- Applies:
  - `KMeans` with 2 clusters
  - `DBSCAN` for density-based clustering
- Uses a sample subset for DBSCAN to reduce processing time.
- Visualizes clusters using the first two transformed features.

**Techniques used**
- `KMeans`
- `DBSCAN`
- `StandardScaler`

**Output**
- Cluster labels for traffic records.
- K-Means cluster visualization.
- DBSCAN cluster visualization.
- Noise points from DBSCAN shown as suspicious/anomalous points.

### Week 6: Malware Classification

**Lab objective**
- Implement malware classification using feature extraction and supervised learning models such as Random Forest and SVM.

**Program**
- `week6/p6.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Uses the NSL-KDD dataset as a labeled cybersecurity classification dataset.
- Converts the label into binary form.
- Encodes categorical attributes.
- Scales the feature space.
- Trains two models:
  - Random Forest
  - SVM
- Compares their classification results.
- Extracts feature importance from the Random Forest model.

**Techniques used**
- `RandomForestClassifier`
- `SVC`
- `classification_report`

**Output**
- Accuracy for Random Forest and SVM.
- Classification report for both models.
- Confusion matrix heatmap for each model.
- Horizontal bar chart of top 10 important features from Random Forest.

### Week 7: Malware Behavior Analysis with PCA

**Lab objective**
- Perform malware behavior analysis using unsupervised learning and dimensionality reduction techniques.

**Program**
- `week7/p7.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Uses the NSL-KDD traffic records as high-dimensional behavior data.
- Encodes categorical attributes.
- Scales all features.
- Applies PCA to reduce the data into 2 principal components.
- Uses labels only for coloring the final visualization.
- Restricts the visualization subset to improve speed.

**Techniques used**
- `PCA`
- `LabelEncoder`
- `StandardScaler`

**Output**
- Explained variance ratio of principal components.
- 2D PCA visualization separating normal and attack behavior patterns.

### Week 8: Phishing URL Detection

**Lab objective**
- Implement phishing URL detection using machine learning with lexical and content-based features.

**Program**
- `week8/p8.py`

**Dataset used**
- `datasets/dataset_full.csv`

**What the program does**
- Loads the phishing dataset.
- Uses the `phishing` column as the target variable.
- Scales engineered URL-related features.
- Trains:
  - Logistic Regression
  - Random Forest
- Evaluates both models.
- Extracts feature importance from the Random Forest model.

**Techniques used**
- `LogisticRegression`
- `RandomForestClassifier`
- `StandardScaler`

**Output**
- Accuracy values for both models.
- Classification reports.
- Confusion matrix heatmaps.
- Top 10 important URL features chart.

### Week 9: Adversarial Attack Simulation

**Lab objective**
- Simulate adversarial attacks on machine learning models and demonstrate model robustness evaluation.

**Program**
- `week9/p9.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads and preprocesses the NSL-KDD dataset.
- Trains a Decision Tree model on clean data.
- Measures baseline accuracy on the test set.
- Adds random noise to test samples to simulate an adversarial-style perturbation.
- Evaluates the same model on the modified test data.
- Compares original and attacked performance.

**Techniques used**
- `DecisionTreeClassifier`
- Feature scaling
- Noise-based attack simulation

**Output**
- Original accuracy.
- Accuracy after attack.
- Accuracy drop showing the effect of perturbed input data.

### Week 10: PCAP / BinetFlow Analysis for Botnet Detection

**Lab objective**
- Analyze network traffic captures and extract features for botnet detection using classification or clustering methods.

**Program**
- `week10/p10.py`

**Dataset used**
- `datasets/capture20110810.binetflow`

**What the program does**
- Loads a BinetFlow traffic file.
- Prints dataset shape and available columns.
- Drops identifier columns such as start time and addresses when present.
- Encodes all remaining values numerically.
- Scales the transformed dataset.
- Uses K-Means clustering to divide traffic into two groups.
- Interprets the two clusters as normal traffic and suspicious/botnet traffic for visualization.

**Techniques used**
- `LabelEncoder`
- `StandardScaler`
- `KMeans`

**Output**
- Dataset shape and column names.
- Cluster labels for sampled traffic flows.
- Scatter plot showing normal traffic vs suspicious or botnet-like traffic.

### Week 11: Brute-Force Detection from Logs

**Lab objective**
- Design a predictive model to detect brute-force or penetration attack attempts from log or network data.

**Program**
- `week11/p11.py`

**Dataset used**
- `datasets/auth.log`

**What the program does**
- Reads authentication log lines.
- Extracts IP addresses and timestamps using regular expressions.
- Identifies failed password attempts and successful logins.
- Expands multi-failure log entries into multiple records.
- Counts failed attempts per IP address.
- Flags IPs whose failed attempts exceed a threshold of 5.
- Visualizes the most suspicious IP addresses.

**Techniques used**
- Regular expressions
- `pandas` grouping and aggregation
- Bar chart visualization

**Output**
- Parsed log summary shape.
- List of suspicious IP addresses with their failed-attempt counts.
- Bar chart of the top brute-force attackers.

### Week 12: Hybrid Intrusion Detection System

**Lab objective**
- Build and test a hybrid intrusion detection system combining supervised and unsupervised approaches for adaptive security.

**Program**
- `week12/p12.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Preprocesses the NSL-KDD dataset into binary attack detection form.
- Trains a supervised `DecisionTreeClassifier` for known attack patterns.
- Trains an unsupervised `IsolationForest` for anomaly detection.
- Combines both outputs using a hybrid rule:
  - if either model flags an attack, the final prediction becomes attack
- Compares supervised, unsupervised, and hybrid accuracy.

**Techniques used**
- `DecisionTreeClassifier`
- `IsolationForest`
- Hybrid decision logic

**Output**
- Supervised model accuracy.
- Unsupervised approximate accuracy.
- Final hybrid IDS accuracy.

### Week 13: Explainable AI with SHAP

**Lab objective**
- Implement feature engineering and model explainability techniques such as SHAP or LIME for AI-driven cyber threat detection systems.

**Program**
- `week13/p13.py`

**Dataset used**
- `datasets/KDDTrain+.txt`

**What the program does**
- Loads and preprocesses the NSL-KDD dataset.
- Converts categorical features to numeric form and scales them.
- Trains a `RandomForestClassifier`.
- Uses SHAP to explain how features contribute to model predictions.
- Creates summary explanations for a subset of the test data to keep execution practical.

**Techniques used**
- `RandomForestClassifier`
- `shap.TreeExplainer`
- SHAP summary plots

**Output**
- SHAP summary plot for feature contribution across samples.
- SHAP bar plot showing overall feature importance.
- An explainability-oriented view of why the model predicts attack vs normal.

## Installation and Setup

### 1. Python Version

Use Python `3.10+` for smooth compatibility with the libraries used in these scripts.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv cyber_env
.\cyber_env\Scripts\Activate.ps1
```

### 3. Install Required Packages

```powershell
pip install pandas numpy matplotlib seaborn scikit-learn shap
```

If `shap` gives installation issues on your machine, upgrade `pip` first:

```powershell
python -m pip install --upgrade pip
pip install shap
```

### 4. Folder Placement

Keep the existing repository structure unchanged because the scripts use relative dataset paths such as:

- `../datasets/KDDTrain+.txt`
- `../datasets/dataset_full.csv`
- `../datasets/capture20110810.binetflow`
- `../datasets/auth.log`

This means each script should be run from inside its own week folder, or the path logic should be adjusted if you run them differently.

### 5. How to Run

Examples:

```powershell
cd week1
python p1.py
```

```powershell
cd week8
python p8.py
```

```powershell
cd week13
python p13.py
```

## Expected Outputs Summary

This section gives a quick output view across all weeks.

| Week | Program | Main Output |
| --- | --- | --- |
| 1 | `p1.py` | Cleaned dataset summary and multiple plots for attack pattern visualization |
| 2 | `p2.py` | Accuracy, classification report, and confusion matrices for 3 classifiers |
| 3 | `p3.py` | Detected anomalies count, approximate accuracy, anomaly scatter plot |
| 4 | `p4.py` | IDS evaluation metrics and confusion matrix |
| 5 | `p5.py` | Cluster labels and cluster visualizations for K-Means and DBSCAN |
| 6 | `p6.py` | Malware/benign classification metrics and feature-importance graph |
| 7 | `p7.py` | PCA explained variance and 2D reduced-space visualization |
| 8 | `p8.py` | Phishing prediction performance and important URL feature chart |
| 9 | `p9.py` | Original accuracy, attacked accuracy, and robustness comparison |
| 10 | `p10.py` | Cluster-based suspicious traffic detection and visualization |
| 11 | `p11.py` | Suspicious IP list and brute-force attacker bar chart |
| 12 | `p12.py` | Supervised vs unsupervised vs hybrid IDS accuracy comparison |
| 13 | `p13.py` | SHAP explainability plots for model interpretation |

## Notes

- The lab document mentions a general cybersecurity or spam/phishing objective in some weeks. The implementations in this repository mostly use the datasets already available in the `datasets/` folder, especially `KDDTrain+.txt` and `dataset_full.csv`.
- Week 10 uses a `.binetflow` file rather than a raw `.pcap` file, but it still serves the same lab purpose of traffic-based botnet analysis.
- Week 13 implements SHAP-based explainability specifically; LIME is mentioned in the lab document as an example, but it is not used in the current code.
- `datasets/spam.csv` is available in the repository, but the current Week 2 implementation is based on phishing-feature classification rather than text-based spam detection.

## Conclusion

This repository provides a full week-wise laboratory workflow for applying AI and machine learning concepts to cybersecurity problems. The programs cover preprocessing, classification, anomaly detection, clustering, intrusion detection, phishing analysis, adversarial robustness, log analysis, hybrid models, and explainable AI using practical datasets and visual outputs.
