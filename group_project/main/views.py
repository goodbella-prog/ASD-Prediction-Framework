from django.shortcuts import render
from .forms import PredictionForm
from .models import Prediction
from .ml.predictor import predict_asd
from .ml.explainer import explain_prediction
from .ml.predictor import preprocess_for_explanation



def home(request):
    return render(request, "main/home.html")


def predict(request):
    if request.method == "POST":
        post_data = request.POST.copy()

        # Automatically set age group
        post_data["age_desc"] = "18 and more"

        # Calculate AQ score automatically
        try:
            post_data["result"] = (
                int(post_data.get("A1_Score", 0)) +
                int(post_data.get("A2_Score", 0)) +
                int(post_data.get("A3_Score", 0)) +
                int(post_data.get("A4_Score", 0)) +
                int(post_data.get("A5_Score", 0)) +
                int(post_data.get("A6_Score", 0)) +
                int(post_data.get("A7_Score", 0)) +
                int(post_data.get("A8_Score", 0)) +
                int(post_data.get("A9_Score", 0)) +
                int(post_data.get("A10_Score", 0))
            )
        except ValueError:
            post_data["result"] = 0

        form = PredictionForm(post_data)

        if form.is_valid():

            data = form.cleaned_data

            prediction, confidence = predict_asd(data)

            processed = preprocess_for_explanation(data)

            explanation = explain_prediction(processed)
            

            

            result_text = (
                "ASD Detected"
                if prediction == 1
                else "No ASD Detected"
            )

            prediction_obj = form.save(commit=False)
            prediction_obj.prediction = result_text
            prediction_obj.save()

            return render(
    request,
    "main/result.html",
    {
        "prediction": result_text,
        "confidence": confidence,
        "explanation": explanation,
    },
)


    else:
        form = PredictionForm()
    

    return render(request, "main/predict.html", {"form": form})

def evaluation(request):
    return render(request, "main/evaluation.html")