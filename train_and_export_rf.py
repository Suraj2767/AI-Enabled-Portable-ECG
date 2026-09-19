import wfdb
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

record_name = "100"

record = wfdb.rdrecord(record_name, pn_dir="mitdb")
ecg = record.p_signal[:, 0]
fs = int(record.fs)

annotation = wfdb.rdann(record_name, "atr", pn_dir="mitdb")

before = int(0.25 * fs)
after = int(0.45 * fs)

X = []
y = []

for sample, symbol in zip(annotation.sample, annotation.symbol):

    if symbol not in ["N", "A"]:
        continue

    start = sample - before
    end = sample + after

    if start < 0 or end > len(ecg):
        continue

    beat = ecg[start:end]

    if len(beat) != 252:
        continue

    mean = np.mean(beat)
    std = np.std(beat)
    maximum = np.max(beat)
    minimum = np.min(beat)
    ptp = np.ptp(beat)
    rms = np.sqrt(np.mean(beat ** 2))

    features = [
        mean,
        std,
        maximum,
        minimum,
        ptp,
        rms
    ]

    X.append(features)

    if symbol == "N":
        y.append(0)
    else:
        y.append(1)

X = np.array(X)
y = np.array(y)

normal_indices = np.where(y == 0)[0]
abnormal_indices = np.where(y == 1)[0]

n = min(len(normal_indices), len(abnormal_indices))

normal_indices = normal_indices[:n]
abnormal_indices = abnormal_indices[:n]

selected_indices = np.concatenate([
    normal_indices,
    abnormal_indices
])

X = X[selected_indices]
y = y[selected_indices]

print("Sampling frequency:", fs)
print("Beat samples:", X.shape[0])
print("Feature count:", X.shape[1])
print("Normal beats:", np.sum(y == 0))
print("Abnormal beats:", np.sum(y == 1))

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", accuracy * 100, "%")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["NORMAL", "ABNORMAL"]
))

joblib.dump(model, "ecg_random_forest.joblib")

print("\nModel saved as:")
print("ecg_random_forest.joblib")