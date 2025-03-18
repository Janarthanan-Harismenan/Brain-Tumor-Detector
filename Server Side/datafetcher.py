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


def encode_image_to_base64(image: Image.Image) -> str:
    """Convert an image to a base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@router.post("/predict")
def predict(file: UploadFile = File(...)):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    result = service.predict(image)
    
    # Encode image as base64 and integrate it inside result
    result["image"] = encode_image_to_base64(image)
    
    result = {
            "result": {
                "image": result["image"],
                "probability": result["probability"],
                "tumor_detected": result["tumor_detected"]
            }
        }
    
    return result


@router.post("/predict/save")
def predict_and_save(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    result = service.predict(image)
    
    # Encode image as base64 and integrate it inside result
    result["image"] = encode_image_to_base64(image)
    
    # Create a Prediction instance, storing the image as binary data
    prediction = Prediction(
        user_id=user.id,
        image_data=contents,
        probability=result["probability"],
        tumor_detected=str(result["tumor_detected"])
    )
    
    # Add and commit the prediction to the database
    db.add(prediction)
    db.commit()
    
    return {"message": "Prediction saved successfully", "result": result}


@router.get("/predictions")
def get_predictions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    predictions = db.query(Prediction).filter(Prediction.user_id == user.id).all()
    
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this user")

    result = []
    for pred in predictions:
        image_data = pred.image_data  # Get the binary image data
        
        # Encode image as base64 if present and integrate it inside result
        base64_image = base64.b64encode(image_data).decode("utf-8") if image_data else None
        
        result.append({
            "id": pred.id,
            "result": {
                "image": base64_image,
                "probability": pred.probability,
                "tumor_detected": pred.tumor_detected
            }
        })
    
    return result
