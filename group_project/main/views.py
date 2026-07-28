from django.shortcuts import render
from .forms import PredictionForm
from .models import Prediction
from .ml.predictor import predict_asd
from .ml.explainer import explain_prediction
from .ml.predictor import preprocess_for_explanation
from django.http import HttpResponse
from django.db.models import Q
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet




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
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from django.http import HttpResponse
from datetime import datetime


def export_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ASD_Screening_Report.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#CC5500")

    heading = styles["Heading2"]

    body = styles["BodyText"]

    story = []

    prediction = request.GET.get("prediction", "Unknown")
    confidence = float(request.GET.get("confidence", 0))

    # Calculate risk level
    if prediction == "ASD Detected":
        if confidence >= 80:
            risk = "High"
        elif confidence >= 60:
            risk = "Moderate"
        else:
            risk = "Low"
    else:
        risk = "Low"

    # ---------------- Title ----------------

    story.append(
        Paragraph(
            "Explainable AI-Based Prediction Framework for Autism Spectrum Disorder",
            title_style,
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "<b>AI Screening Report</b>",
            heading,
        )
    )

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            body,
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    # ---------------- Results ----------------

    story.append(
        Paragraph(f"<b>Prediction Result:</b> {prediction}", heading)
    )

    story.append(
        Paragraph(f"<b>Confidence Score:</b> {confidence:.2f}%", heading)
    )

    story.append(
        Paragraph(f"<b>Risk Level:</b> {risk}", heading)
    )

    story.append(Spacer(1, 0.25 * inch))

    # ---------------- AI Explanation ----------------

    story.append(
        Paragraph("Explainable AI Summary", heading)
    )

    story.append(
        Paragraph(
            "The machine learning model analysed the user's AQ-10 responses "
            "together with demographic information before generating this prediction. "
            "The web application provides a detailed SHAP analysis showing the contribution "
            "of each feature to the prediction.",
            body,
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ---------------- Recommendation ----------------

    story.append(
        Paragraph("Recommendation", heading)
    )

    story.append(
        Paragraph(
            "This report is intended for screening purposes only. "
            "It should not be used as a substitute for a professional "
            "medical diagnosis. Individuals with concerns should consult "
            "a qualified healthcare professional for comprehensive assessment.",
            body,
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # ---------------- Disclaimer ----------------

    story.append(
        Paragraph(
            "<b>Disclaimer:</b> This report was automatically generated by the "
            "Explainable AI-Based Prediction Framework for Autism Spectrum Disorder.",
            body,
        )
    )

    doc.build(story)

    return response

def history(request):

    search = request.GET.get("search")

    predictions = Prediction.objects.all().order_by("-created_at")

    if search:
        predictions = predictions.filter(
            Q(prediction__icontains=search) |
            Q(gender__icontains=search) |
            Q(contry_of_res__icontains=search)
        )

    return render(
        request,
        "main/history.html",
        {
            "predictions": predictions,
        }
    )
from django.db.models import Count
from .models import Prediction


def dashboard(request):
    total = Prediction.objects.count()

    detected = Prediction.objects.filter(
        prediction="ASD Detected"
    ).count()

    not_detected = Prediction.objects.filter(
        prediction="No ASD Detected"
    ).count()

    context = {
        "total": total,
        "detected": detected,
        "not_detected": not_detected,
    }

    return render(
        request,
        "main/dashboard.html",
        context,
    )
def about(request):
    return render(request, "main/about.html")