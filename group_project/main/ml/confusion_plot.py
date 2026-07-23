import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

train_data = pd.read_csv("train.csv", sep="\t")
test_data = pd.read_csv("test.csv", sep="\t")

categorical_columns = [
    "gender",
    "ethnicity",
    "jaundice",
    "austim",
    "contry_of_res",
    "used_app_before",
    "age_desc",
    "relation"
]

for col in categorical_columns:
    encoder = LabelEncoder()
    encoder.fit(pd.concat([train_data[col], test_data[col]]))
    train_data[col] = encoder.transform(train_data[col])

X = train_data.drop(columns=["ID", "Class/ASD"])
y = train_data["Class/ASD"]

X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load("model.pkl")

ConfusionMatrixDisplay.from_estimator(
    model,
    X_val,
    y_val
)

plt.title("Confusion Matrix")

plt.savefig("confusion_matrix.png", dpi=300)

print("Confusion Matrix saved successfully!")