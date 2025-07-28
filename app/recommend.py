def recommend(data: dict):
    recommendations = []
    if data["cholesterol"] > 240:
        recommendations.append("Reduce saturated fats.")
    if data["blood_pressure"] > 140:
        recommendations.append("Consider a low-sodium diet.")
    if data["glucose"] > 126:
        recommendations.append("Monitor for diabetes.")
    if not recommendations:
        recommendations.append("Keep up the healthy lifestyle!")
    return recommendations
