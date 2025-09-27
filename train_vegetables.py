# Training script cho Vegetable Classification
from ultralytics import YOLO
import torch

def train_vegetable_classifier():
    print("🥬 Training Vegetable Classification Model")
    print("=" * 50)
    
    # Check GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load model
    model = YOLO('yolov8n-cls.pt')  # Classification model
    
    # Training arguments
    args = {
        'data': 'vegetable_dataset',
        'epochs': 100,
        'imgsz': 224,  # Standard cho classification
        'batch': 32,
        'device': device,
        'workers': 4,
        'patience': 20,
        'save_period': 10,
        'project': 'vegetable_classification',
        'name': 'yolov8n_vegetables',
        'exist_ok': True,
        
        # Augmentation
        'hsv_h': 0.015,
        'hsv_s': 0.7, 
        'hsv_v': 0.4,
        'degrees': 15,
        'translate': 0.1,
        'scale': 0.5,
        'fliplr': 0.5,
        'flipud': 0.0,
        'mosaic': 0.0,  # Tắt mosaic cho classification
        'mixup': 0.2,
        
        # Optimizer
        'optimizer': 'AdamW',
        'lr0': 0.001,
        'weight_decay': 0.0005,
        'warmup_epochs': 5,
        
        # Other
        'dropout': 0.2,
        'plots': True,
        'val': True,
    }
    
    # Start training
    print("🚀 Starting training...")
    results = model.train(**args)
    
    print("\n✅ Training completed!")
    print(f"Best model saved at: runs/classify/yolov8n_vegetables/weights/best.pt")
    
    # Validate
    print("\n📊 Running validation...")
    metrics = model.val()
    print(f"Top-1 Accuracy: {metrics.top1:.3f}")
    print(f"Top-5 Accuracy: {metrics.top5:.3f}")
    
    return model, results

def test_model():
    """Test trained model"""
    print("\n🧪 Testing model...")
    
    # Load best model
    model = YOLO('runs/classify/yolov8n_vegetables/weights/best.pt')
    
    # Test trên test set
    results = model.val(data='vegetable_dataset', split='test')
    print(f"Test Accuracy: {results.top1:.3f}")
    
    return results

def predict_single_image(image_path):
    """Predict một ảnh"""
    model = YOLO('runs/classify/yolov8n_vegetables/weights/best.pt')
    
    results = model(image_path)
    
    # Lấy prediction
    pred = results[0]
    class_id = pred.probs.top1
    confidence = pred.probs.top1conf.item()
    class_name = pred.names[class_id]
    
    print(f"Prediction: {class_name} ({confidence:.3f})")
    return class_name, confidence

if __name__ == "__main__":
    # Train model
    model, results = train_vegetable_classifier()
    
    # Test model  
    test_results = test_model()
    
    print("\n🎉 All done! Model ready for use.")
