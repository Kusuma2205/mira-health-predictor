def get_health_prediction(full_name, dob, glucose, haemoglobin, cholesterol):
    issues = []
    recommendations = []
    risk_level = "Low"

    if glucose < 70:
        issues.append("Glucose is LOW (Hypoglycaemia risk)")
        recommendations.append("Increase carbohydrate intake and consult a doctor.")
        risk_level = "Moderate"
    elif 70 <= glucose <= 99:
        issues.append("Glucose is NORMAL")
    elif 100 <= glucose <= 125:
        issues.append("Glucose is BORDERLINE HIGH (Pre-diabetic range)")
        recommendations.append("Reduce sugar intake and monitor glucose regularly.")
        risk_level = "Moderate"
    elif glucose >= 126:
        issues.append("Glucose is HIGH (Diabetic risk)")
        recommendations.append("Immediate medical consultation recommended.")
        risk_level = "High"

    if haemoglobin < 12:
        issues.append("Haemoglobin is LOW (Anaemia risk)")
        recommendations.append("Increase iron-rich foods and consider supplementation.")
        if risk_level != "High":
            risk_level = "Moderate"
    elif 12 <= haemoglobin <= 17.5:
        issues.append("Haemoglobin is NORMAL")
    else:
        issues.append("Haemoglobin is HIGH (Polycythaemia risk)")
        recommendations.append("Consult a haematologist for further evaluation.")
        if risk_level != "High":
            risk_level = "Moderate"

    if cholesterol < 200:
        issues.append("Cholesterol is NORMAL")
    elif 200 <= cholesterol <= 239:
        issues.append("Cholesterol is BORDERLINE HIGH")
        recommendations.append("Adopt a low-fat diet and increase physical activity.")
        if risk_level == "Low":
            risk_level = "Moderate"
    else:
        issues.append("Cholesterol is HIGH (Cardiovascular risk)")
        recommendations.append("Consult a cardiologist and begin cholesterol management.")
        risk_level = "High"

    assessment = " | ".join(issues)
    advice = " ".join(recommendations) if recommendations else "All values are within normal range. Maintain a healthy lifestyle."
    return f"Assessment: {assessment}. Overall Risk: {risk_level}. Recommendation: {advice}"
