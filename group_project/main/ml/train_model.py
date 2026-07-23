import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_PATH = os.path.join(BASE_DIR, "train.csv")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

df = pd.read_csv(TRAIN_PATH, sep="\t")

print("Dataset loaded successfully!")
print(df.head())

# -------------------------------------------------
# Drop ID column
# -------------------------------------------------

if "ID" in df.columns:
    df.drop("ID", axis=1, inplace=True)

# -------------------------------------------------
# Encode categorical columns
# -------------------------------------------------

categorical_columns = [
    "gender",
    "ethnicity",
    "jaundice",
    "austim",
    "contry_of_res",
    "used_app_before",
    "age_desc",
    "relation",
]

encoders = {}

for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column].astype(str))
    encoders[column] = encoder

# -------------------------------------------------
# Features and Target
# -------------------------------------------------

X = df.drop("Class/ASD", axis=1)
y = df["Class/ASD"]

# -------------------------------------------------
# Train/Test Split
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# -------------------------------------------------
# Train Model
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------------------------
# Evaluate
# -------------------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy: {accuracy * 100:.2f}%")

# -------------------------------------------------
# Save Model
# -------------------------------------------------

joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(encoders, os.path.join(BASE_DIR, "encoder.pkl"))

print("\nModel saved successfully.")
print("Encoder saved successfully.")