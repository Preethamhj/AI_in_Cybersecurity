# ============================================
# WEEK 11: BRUTE FORCE DETECTION
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

            # Extract IP, timestamp, status code
            match = re.search(r'(\S+) - - \[(.*?)\] ".*?" (\d+)', line)

            if match:
                ip = match.group(1)
                timestamp = match.group(2)
                status = int(match.group(3))

                # Success = 200, Fail = others
                success = 1 if status == 200 else 0

                data.append([ip, timestamp, success])

    df = pd.DataFrame(data, columns=['ip', 'timestamp', 'success'])

    # Convert timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    df = df.dropna()

    print("Logs Loaded:", df.shape)

    return df


# ============================================
# DETECT BRUTE FORCE
# ============================================

def detect_bruteforce(df):

    # Count failed attempts per IP
    failed = df[df['success'] == 0]

    attack_counts = failed.groupby('ip').size()

    # Threshold (you can tune this)
    threshold = 10

    attackers = attack_counts[attack_counts > threshold]

    print("\n⚠️ Suspicious IPs (Brute Force):")
    print(attackers)

    return attackers


# ============================================
# VISUALIZATION
# ============================================

def visualize(attackers):

    if len(attackers) == 0:
        print("No brute force attacks detected.")
        return

    plt.figure(figsize=(8,5))

    attackers.plot(kind='bar')

    plt.title("Brute Force Attack Attempts per IP")
    plt.xlabel("IP Address")
    plt.ylabel("Failed Attempts")

    plt.xticks(rotation=45)
    plt.show()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    df = load_logs("../datasets/auth.txt")

    attackers = detect_bruteforce(df)

    visualize(attackers)

    print("\n✅ Week 11 Completed Successfully!")