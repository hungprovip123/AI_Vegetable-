# Test và sử dụng model rau đã train
from ultralytics import YOLO
import os
import json
from pathlib import Path

def find_best_model():
    """Tìm model đã train"""
    possible_paths = [
        'vegetable_classification/yolov8n_vegetables/weights/best.pt',
        'runs/classify/yolov8n_vegetables/weights/best.pt',
        'runs/classify/yolov8n_vegetables2/weights/best.pt',
        'runs/classify/yolov8n_vegetables3/weights/best.pt'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found model at: {path}")
            return path
    
    print("❌ No trained model found!")
    return None

def load_class_mapping():
    """Load class mapping"""
    mapping_file = 'vegetable_dataset/class_mapping.json'
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def test_model_on_dataset():
    """Test model trên test set"""
    model_path = find_best_model()
    if not model_path:
        return
    
    print("🧪 Testing model on test dataset...")
    model = YOLO(model_path)
    
    # Test trên test set
    results = model.val(data='vegetable_dataset', split='test')
    print(f"📊 Test Results:")
    print(f"   Top-1 Accuracy: {results.top1:.3f}")
    print(f"   Top-5 Accuracy: {results.top5:.3f}")
    
    return results

def predict_single_image(image_path):
    """Predict một ảnh rau"""
    model_path = find_best_model()
    if not model_path:
        return
    
    model = YOLO(model_path)
    class_mapping = load_class_mapping()
    
    print(f"🔍 Predicting: {image_path}")
    
    results = model(image_path, verbose=False)
    
    # Lấy prediction
    pred = results[0]
    
    # Top 3 predictions
    probs = pred.probs.data
    top3_indices = probs.argsort(descending=True)[:3]
    
    print("📋 Top 3 predictions:")
    for i, idx in enumerate(top3_indices):
        class_name = pred.names[idx.item()]
        confidence = probs[idx].item()
        print(f"   {i+1}. {class_name}: {confidence:.3f}")
    
    return results

def batch_predict_folder(folder_path):
    """Predict tất cả ảnh trong folder"""
    model_path = find_best_model()
    if not model_path:
        return
    
    model = YOLO(model_path)
    
    # Lấy tất cả ảnh trong folder
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    images = []
    
    for ext in image_extensions:
        images.extend(list(Path(folder_path).glob(f'*{ext}')))
        images.extend(list(Path(folder_path).glob(f'*{ext.upper()}')))
    
    if not images:
        print(f"❌ No images found in {folder_path}")
        return
    
    print(f"🔍 Predicting {len(images)} images in {folder_path}")
    
    results = model(images, verbose=False)
    
    # Tổng hợp kết quả
    predictions = {}
    for i, result in enumerate(results):
        image_name = images[i].name
        
        probs = result.probs.data
        top1_idx = probs.argmax()
        top1_class = result.names[top1_idx.item()]
        top1_conf = probs[top1_idx].item()
        
        predictions[image_name] = {
            'class': top1_class,
            'confidence': top1_conf
        }
    
    # Hiển thị kết quả
    print("\n📊 Prediction Results:")
    for img_name, pred in predictions.items():
        print(f"   {img_name}: {pred['class']} ({pred['confidence']:.3f})")
    
    # Thống kê
    class_counts = {}
    for pred in predictions.values():
        class_name = pred['class']
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    
    print(f"\n📈 Class Distribution:")
    for class_name, count in sorted(class_counts.items()):
        print(f"   {class_name}: {count} ảnh")
    
    return predictions

def demo_predictions():
    """Demo predictions với một số ảnh từ dataset gốc"""
    print("🎯 Demo Predictions")
    print("="*50)
    
    # Test với một số ảnh từ dataset gốc
    test_folders = ['anhtrainAi/Ca_chua', 'anhtrainAi/Ca_rot', 'anhtrainAi/Cai_thao']
    
    for folder in test_folders:
        if os.path.exists(folder):
            print(f"\n🥬 Testing folder: {folder}")
            
            # Lấy 1 ảnh đầu tiên để test
            for file in os.listdir(folder):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(folder, file)
                    predict_single_image(image_path)
                    break
            break

def show_model_info():
    """Hiển thị thông tin model"""
    model_path = find_best_model()
    if not model_path:
        return
    
    model = YOLO(model_path)
    
    print("📋 Model Information:")
    print(f"   Model path: {model_path}")
    print(f"   Number of classes: {len(model.names)}")
    print(f"   Classes: {list(model.names.values())[:10]}...")  # Show first 10
    
    # Model summary
    print("\n🔧 Model Summary:")
    model.info()

if __name__ == "__main__":
    print("🥬 Vegetable Classification Model Testing")
    print("="*60)
    
    # 1. Show model info
    show_model_info()
    print("\n" + "="*40 + "\n")
    
    # 2. Test model on dataset
    test_model_on_dataset()
    print("\n" + "="*40 + "\n")
    
    # 3. Demo predictions
    demo_predictions()
    
    print("\n🎉 Testing completed!")
    print("\n📝 Usage examples:")
    print("   python test_vegetable_model.py")
    print("   predict_single_image('path/to/image.jpg')")
    print("   batch_predict_folder('path/to/folder')")
