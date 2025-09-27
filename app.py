# FastAPI Web App & API cho Vegetable Classification
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO
import cv2
import numpy as np
import json
import os
import io
from PIL import Image
import base64
import uvicorn
from pathlib import Path
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create lifespan context
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await startup()
    yield
    # Shutdown  
    await shutdown()

# Initialize FastAPI app
app = FastAPI(
    title="🥬 Vietnamese Vegetable Classification API",
    description="AI-powered Vietnamese vegetable recognition system using YOLOv8",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global variables
model = None
class_names = None

def find_model_path():
    """Tìm model đã train"""
    possible_paths = [
        'vegetable_classification/yolov8n_vegetables/weights/best.pt',
        'runs/classify/yolov8n_vegetables/weights/best.pt',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def load_class_mapping():
    """Load class names mapping"""
    mapping_file = 'vegetable_dataset/class_mapping.json'
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

async def startup():
    """Load model khi start app"""
    global model, class_names
    
    logger.info("🚀 Starting Vegetable Classification API...")
    
    # Load model - try download if not found
    model_path = find_model_path()
    if not model_path:
        logger.info("📥 Model not found locally, attempting download...")
        try:
            from download_model import download_model
            if download_model():
                model_path = find_model_path()
        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
        
        if not model_path:
            logger.warning("⚠️ Using default YOLOv8 model for demo")
            model_path = "yolov8n-cls.pt"  # Will auto-download
    
    try:
        model = YOLO(model_path)
        logger.info(f"✅ Model loaded from: {model_path}")
        
        # Load class names
        class_mapping = load_class_mapping()
        if class_mapping:
            class_names = class_mapping
            logger.info(f"✅ Loaded {len(class_names)} vegetable classes")
        else:
            class_names = {str(i): name for i, name in model.names.items()}
            
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise RuntimeError(f"Failed to load model: {e}")

async def shutdown():
    """Cleanup khi shutdown"""
    logger.info("🛑 Shutting down Vegetable Classification API...")

def process_image(image_data: bytes) -> Image.Image:
    """Process uploaded image"""
    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        max_size = 1024
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

def predict_vegetable(image: Image.Image, top_k: int = 5) -> Dict:
    """Predict vegetable from image"""
    try:
        # Run prediction
        results = model(image, verbose=False)
        result = results[0]
        
        # Get probabilities
        probs = result.probs.data.numpy()
        
        # Get top-k predictions
        top_indices = probs.argsort()[::-1][:top_k]
        
        predictions = []
        for idx in top_indices:
            class_name = result.names[idx]
            confidence = float(probs[idx])
            
            predictions.append({
                "class": class_name,
                "confidence": confidence,
                "percentage": f"{confidence * 100:.1f}%"
            })
        
        return {
            "success": True,
            "predictions": predictions,
            "top_prediction": predictions[0] if predictions else None
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

# Web Interface Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Trang chủ với giao diện upload ảnh"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Vietnamese Vegetable Classification",
        "total_classes": len(class_names) if class_names else 0
    })

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Trang thông tin"""
    return templates.TemplateResponse("about.html", {
        "request": request,
        "title": "About - Vegetable Classification"
    })

# API Routes
@app.post("/api/predict")
async def api_predict(file: UploadFile = File(...), top_k: int = 5):
    """
    API endpoint để predict vegetable từ ảnh upload
    
    - **file**: Image file (jpg, png, etc.)
    - **top_k**: Number of top predictions to return (default: 5)
    """
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_data = await file.read()
        image = process_image(image_data)
        
        # Make prediction
        result = predict_vegetable(image, top_k)
        
        # Add metadata
        result["metadata"] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "image_size": image.size,
            "model_classes": len(class_names) if class_names else 0
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/api/predict-base64")
async def api_predict_base64(data: dict):
    """
    API endpoint để predict từ base64 image
    
    Body: {"image": "base64_string", "top_k": 5}
    """
    
    try:
        # Validate input
        if "image" not in data:
            raise HTTPException(status_code=400, detail="Missing 'image' field")
        
        base64_str = data["image"]
        top_k = data.get("top_k", 5)
        
        # Remove data URL prefix if present
        if base64_str.startswith('data:image'):
            base64_str = base64_str.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_str)
        image = process_image(image_data)
        
        # Make prediction
        result = predict_vegetable(image, top_k)
        
        result["metadata"] = {
            "input_type": "base64",
            "image_size": image.size,
            "model_classes": len(class_names) if class_names else 0
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Base64 prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/api/classes")
async def api_get_classes():
    """Get all available vegetable classes"""
    return {
        "success": True,
        "classes": list(class_names.keys()) if class_names else [],
        "total": len(class_names) if class_names else 0
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "classes_loaded": class_names is not None,
        "total_classes": len(class_names) if class_names else 0
    }

@app.get("/api/model-info")
async def model_info():
    """Get model information"""
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "YOLOv8n-cls",
        "framework": "Ultralytics",
        "task": "Image Classification", 
        "classes": len(class_names) if class_names else 0,
        "input_size": "224x224",
        "supported_formats": ["jpg", "jpeg", "png", "webp", "bmp"]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Page not found", "detail": "The requested page does not exist"}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "Something went wrong"}
    )

if __name__ == "__main__":
    # Create directories if not exist
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    print("🥬 Starting Vietnamese Vegetable Classification Web App")
    print("="*60)
    print("📱 Web Interface: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("="*60)
    
    import os
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload for production
        log_level="info"
    )

