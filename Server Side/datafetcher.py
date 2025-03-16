import base64
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
import io
from service import TumorDetectionService
from auth import get_current_user
from database import get_db
from models import Prediction

router = APIRouter()
service = TumorDetectionService("Model/cnn-parameters-improvement-02-0.86.keras")

@router.post("/predict")
def predict(file: UploadFile = File(...)):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    result = service.predict(image)
    return result

@router.post("/predict/save")
def predict_and_save(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    contents = file.file.read()  # Read the image data as bytes
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    result = service.predict(image)
    
    # Create a Prediction instance, storing the image as binary data
    prediction = Prediction(
        user_id=user.id,
        image_data=contents,  # Store the image as binary data
        probability=result["probability"],
        tumor_detected=str(result["tumor_detected"])
    )
    
    # Add and commit the prediction to the database
    db.add(prediction)
    db.commit()
    
    return {"message": "Prediction saved successfully", "result": result}

@router.get("/predictions")
def get_predictions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve all saved predictions for the authenticated user, with the image returned as base64-encoded string.
    """
    predictions = db.query(Prediction).filter(Prediction.user_id == user.id).all()
    
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this user")

    result = []
    for pred in predictions:
        image_data = pred.image_data  # Get the binary image data
        
        # If the image data is present, encode it as base64
        if image_data:
            base64_image = base64.b64encode(image_data).decode("utf-8")
            result.append({
                "id": pred.id,
                "image": base64_image,  # Return image as base64 string
                "probability": pred.probability,
                "tumor_detected": pred.tumor_detected
            })
        else:
            result.append({
                "id": pred.id,
                "image": None,  # Return None if the image is missing
                "probability": pred.probability,
                "tumor_detected": pred.tumor_detected
            })

    return result
