import os
import joblib
import shap
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))


def explain_prediction(data):

    sample = pd.DataFrame([data])

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(sample)

    feature_names = sample.columns.tolist()

    feature_labels = {
        "A1_Score": "A1: I often notice small sounds when others do not",
        "A2_Score": "A2: I usually concentrate more on the whole picture than small details",
        "A3_Score": "A3: I find it easy to do more than one thing at once",
        "A4_Score": "A4: If interrupted, I can quickly return to what I was doing",
        "A5_Score": "A5: I find it easy to read between the lines when someone is talking",
        "A6_Score": "A6: I know if someone listening to me is getting bored",
        "A7_Score": "A7: When reading a story, I find it difficult to work out the characters' intentions",
        "A8_Score": "A8: I like collecting information about categories of things",
        "A9_Score": "A9: I find it easy to work out what someone is thinking or feeling",
        "A10_Score": "A10: I find it difficult to work out people's intentions",
        "age": "Age",
        "gender": "Gender",
        "ethnicity": "Ethnicity",
        "jaundice": "History of Jaundice",
        "austim": "Family History of Autism",
        "contry_of_res": "Country of Residence",
        "used_app_before": "Previously Used Screening App",
        "result": "AQ Screening Score",
        "age_desc": "Age Group",
        "relation": "Relationship to Patient",
    }

    display_feature_names = [
        feature_labels.get(feature, feature)
        for feature in feature_names
    ]

    # Handle SHAP output
    if isinstance(shap_values, list):
        values = shap_values[1][0]
        base_value = explainer.expected_value[1]
    else:
        if shap_values.ndim == 3:
            values = shap_values[0, :, 1]
            base_value = explainer.expected_value[1]
        elif shap_values.ndim == 2:
            values = shap_values[0]
            base_value = explainer.expected_value
        else:
            values = shap_values
            base_value = explainer.expected_value

    # Build explanation dictionary
    # Build HTML explanation
    html = """
    <h5 class="mb-3">Top Factors Influencing the Prediction</h5>
    <table class="table table-bordered table-striped">
    <thead>
    <tr>
    <th>Feature</th>
    <th>Impact</th>
    </tr>
    </thead>
    <tbody>
    """

    for feature, value in zip(feature_names, values):

        display_name = feature_labels.get(feature, feature)

        colour = "green" if value < 0 else "red"

        html += f"""
        <tr>
            <td>{display_name}</td>
            <td style="color:{colour}; font-weight:bold;">
                {value:.4f}
            </td>
        </tr>
        """

    html += """
    </tbody>
    </table>

    <h5 class="mt-4">Feature Importance Chart</h5>

    <img src="/static/images/shap_bar.png"
         class="img-fluid rounded shadow">
    """

    return html