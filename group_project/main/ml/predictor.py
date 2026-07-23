import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


model = joblib.load(
    os.path.join(BASE_DIR, "model.pkl")
)

encoders = joblib.load(
    os.path.join(BASE_DIR, "encoder.pkl")
)



def preprocess_input(data):

    processed = data.copy()

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


    for column in categorical_columns:

        value = str(processed[column]).strip()

        encoder = encoders[column]


        if value not in encoder.classes_:

            raise ValueError(
                f"{value} is not valid for {column}"
            )


        processed[column] = encoder.transform(
            [value]
        )[0]


    return processed



def predict_asd(data):

    processed = preprocess_input(data)


    df = pd.DataFrame([processed])


    # keep same order used during training
    if hasattr(model, "feature_names_in_"):
        df = df[model.feature_names_in_]


    prediction = model.predict(df)[0]


    probability = model.predict_proba(df)[0]


    confidence = round(
        max(probability) * 100,
        2
    )


    return prediction, confidence



def preprocess_for_explanation(data):

    return preprocess_input(data)