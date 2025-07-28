from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.predict_heart import predict_risk
from app.recommend import recommend
from app.predict_skin import predict_image
from app.pdf_reports import generate_pdf
from app.gpt_summary import summarize_text
from app.emailer import send_report
from app.database import SessionLocal, PredictionRecord
import joblib
import json
import os

app = FastAPI(title="One Doctor ML API")

# --- API Key Protection ---
API_KEY = "YOUR_SECRET_KEY"

def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# --- Basic Model (joblib) Prediction Setup ---
model_path = os.path.join("models", "model.pkl")
model = joblib.load(model_path)

class BasicInput(BaseModel):
    feature1: float
    feature2: float

# --- Core Input Models ---
class HealthData(BaseModel):
    age: int
    cholesterol: float
    blood_pressure: float
    glucose: float

class TextInput(BaseModel):
    text: str

# --- Routes ---

@app.get("/")
def home():
    return {"message": "OneDoctor ML API is live!"}

@app.post("/basic-predict", dependencies=[Depends(verify_key)])
def basic_predict(data: BasicInput):
    prediction = model.predict([[data.feature1, data.feature2]])
    return {"prediction": int(prediction[0])}

@app.post("/predict-risk", dependencies=[Depends(verify_key)])
def predict(health_data: HealthData):
    result = predict_risk(health_data.dict())
    db = SessionLocal()
    record = PredictionRecord(
        prediction_type="risk",
        result=result,
        input_data=json.dumps(health_data.dict())
    )
    db.add(record)
    db.commit()
    db.close()
    return {"risk_level": result}

@app.post("/recommendations", dependencies=[Depends(verify_key)])
def get_recommendations(health_data: HealthData):
    recs = recommend(health_data.dict())
    return {"recommendations": recs}

@app.post("/analyze-image", dependencies=[Depends(verify_key)])
async def analyze_image(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    result = predict_image(file_path)
    return {"analysis": result}

@app.post("/predict-risk/report", dependencies=[Depends(verify_key)])
def predict_with_report(health_data: HealthData):
    result = predict_risk(health_data.dict())
    pdf_file = generate_pdf(result, health_data.dict())
    return FileResponse(pdf_file, media_type="application/pdf", filename="risk_report.pdf")

@app.post("/predict-risk/report-email", dependencies=[Depends(verify_key)])
def predict_report_email(health_data: HealthData, email: str):
    result = predict_risk(health_data.dict())
    pdf_file = generate_pdf(result, health_data.dict())
    send_report(email, pdf_file)
    return {"message": "Report sent to email."}

@app.post("/summarize", dependencies=[Depends(verify_key)])
def summarize(input_text: TextInput):
    summary = summarize_text(input_text.text)
    return {"summary": summary}
