# ============================================
# WEEK 11: BRUTE FORCE DETECTION (FIXED)
# ============================================

import pandas as pd
import re
import matplotlib.pyplot as plt


# ============================================
# LOAD & PARSE LOG FILE
# ============================================

def load_logs(filepath):

    data = []

    with open(filepath, 'r') as f:
        for line in f:

            # Extract IP
            ip_match = re.findall(r'\d+\.\d+\.\d+\.\d+', line)

            if not ip_match:
                continue

            ip = ip_match[0]

            # Extract timestamp (simple format)
            timestamp_match = re.search(r'^\w+\s+\d+\s+\d+:\d+:\d+', line)

            timestamp = timestamp_match.group(0) if timestamp_match else None

            # Case 1: Multiple failures in one line
            multi_fail = re.search(r'(\d+) more authentication failures', line)

            if multi_fail:
                count = int(multi_fail.group(1))
                success = 0

                for _ in range(count):
                    data.append([ip, timestamp, success])

            # Case 2: Single failed password
            elif "Failed password" in line:
                success = 0
                data.append([ip, timestamp, success])

            # Case 3: Successful login
            elif "Accepted" in line:
                success = 1
                data.append([ip, timestamp, success])

    df = pd.DataFrame(data, columns=['ip', 'timestamp', 'success'])

    print("Logs Loaded:", df.shape)

    return df


# ============================================
# DETECT BRUTE FORCE
# ============================================

def detect_bruteforce(df):

    # Count failed attempts per IP
    failed = df[df['success'] == 0]

    attack_counts = failed.groupby('ip').size()

    # Threshold
    threshold = 5

    attackers = attack_counts[attack_counts > threshold]

    print("\n⚠️ Suspicious IPs (Brute Force):")
    print(attackers)

    return attackers


# ============================================
# VISUALIZATION
# ============================================

def visualize(attackers, top_n=10):

    if len(attackers) == 0:
        print("No brute force attacks detected.")
        return

    # Take top N attackers
    attackers = attackers.sort_values(ascending=False).head(top_n)

    plt.figure(figsize=(10,5))

    attackers.plot(kind='bar')

    plt.title(f"Top {top_n} Brute Force Attackers")
    plt.xlabel("IP Address")
    plt.ylabel("Failed Attempts")

    plt.xticks(rotation=45, fontsize=8)  # cleaner labels
    plt.tight_layout()

    plt.show()

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_logs("../datasets/auth.log")

    attackers = detect_bruteforce(df)

    visualize(attackers)

    print("\n✅ Week 11 Completed Successfully!")