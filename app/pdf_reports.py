from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(prediction: str, input_data: dict, filename: str = "report.pdf"):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "One Doctor Health Prediction Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

    c.drawString(50, 740, "Prediction Result:")
    c.drawString(70, 720, prediction)

    c.drawString(50, 690, "Input Data:")
    y = 670
    for key, value in input_data.items():
        c.drawString(70, y, f"{key}: {value}")
        y -= 20

    c.save()
    return filename
