# Script chuẩn bị dataset rau cho YOLOv8 Classification
import os
import shutil
import yaml
from pathlib import Path
import random
from PIL import Image, ExifTags
import json

def analyze_dataset(source_dir="anhtrainAi"):
    """Phân tích dataset gốc"""
    print("🔍 Analyzing vegetable dataset...")
    
    stats = {}
    total_images = 0
    
    for folder in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder)
        if os.path.isdir(folder_path):
            # Đếm số ảnh trong folder
            image_count = 0
            extensions = {}
            
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.heic', '.avif', '.gif')):
                    image_count += 1
                    ext = file.split('.')[-1].lower()
                    extensions[ext] = extensions.get(ext, 0) + 1
            
            stats[folder] = {
                'count': image_count,
                'extensions': extensions
            }
            total_images += image_count
    
    print(f"📊 Dataset analysis:")
    print(f"   Total classes: {len(stats)}")
    print(f"   Total images: {total_images}")
    print(f"   Average per class: {total_images/len(stats):.1f}")
    
    # Top 10 classes với nhiều ảnh nhất
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['count'], reverse=True)
    print("\n🏆 Top 10 classes với nhiều ảnh nhất:")
    for i, (class_name, info) in enumerate(sorted_stats[:10]):
        print(f"   {i+1:2d}. {class_name:<20}: {info['count']:2d} ảnh")
    
    # Classes với ít ảnh
    low_count = [name for name, info in stats.items() if info['count'] < 8]
    if low_count:
        print(f"\n⚠️ Classes có ít ảnh (<8): {len(low_count)} classes")
        for name in low_count[:5]:  # Show first 5
            print(f"   - {name}: {stats[name]['count']} ảnh")
    
    return stats

def create_yolo_structure(output_dir="vegetable_dataset"):
    """Tạo cấu trúc dataset cho YOLOv8 Classification"""
    print(f"\n📁 Creating YOLO dataset structure in {output_dir}/")
    
    # Tạo cấu trúc thư mục
    dirs = [
        f"{output_dir}/train",
        f"{output_dir}/val", 
        f"{output_dir}/test"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✅ Created train/val/test directories")
    return output_dir

def fix_image_rotation(image_path):
    """Sửa rotation của ảnh dựa vào EXIF data"""
    try:
        image = Image.open(image_path)
        
        # Xử lý EXIF orientation
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
        
        return image
    except:
        return Image.open(image_path)

def convert_and_copy_images(source_dir="anhtrainAi", output_dir="vegetable_dataset", train_ratio=0.7, val_ratio=0.2):
    """Convert và copy ảnh vào cấu trúc YOLO với train/val/test split"""
    print(f"\n🖼️ Converting and organizing images...")
    print(f"   Split ratio - Train: {train_ratio}, Val: {val_ratio}, Test: {1-train_ratio-val_ratio}")
    
    stats = analyze_dataset(source_dir)
    
    # Tạo class mapping
    class_names = sorted(stats.keys())
    class_mapping = {name: idx for idx, name in enumerate(class_names)}
    
    conversion_stats = {
        'converted': 0,
        'skipped': 0,
        'errors': 0,
        'train': 0,
        'val': 0,
        'test': 0
    }
    
    for class_name in class_names:
        print(f"Processing {class_name}...")
        
        # Tạo thư mục cho class trong mỗi split
        for split in ['train', 'val', 'test']:
            class_dir = os.path.join(output_dir, split, class_name)
            os.makedirs(class_dir, exist_ok=True)
        
        # Lấy tất cả ảnh của class
        source_class_dir = os.path.join(source_dir, class_name)
        image_files = []
        
        for file in os.listdir(source_class_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.heic', '.avif')):
                image_files.append(file)
        
        # Shuffle và split
        random.shuffle(image_files)
        n_total = len(image_files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        
        train_files = image_files[:n_train]
        val_files = image_files[n_train:n_train + n_val]
        test_files = image_files[n_train + n_val:]
        
        # Process từng split
        splits = [
            ('train', train_files),
            ('val', val_files), 
            ('test', test_files)
        ]
        
        for split_name, files in splits:
            for i, file in enumerate(files):
                try:
                    source_path = os.path.join(source_class_dir, file)
                    
                    # Đổi extension thành .jpg
                    new_filename = f"{class_name}_{split_name}_{i:03d}.jpg"
                    target_path = os.path.join(output_dir, split_name, class_name, new_filename)
                    
                    # Mở và convert ảnh
                    if file.lower().endswith('.heic'):
                        # HEIC cần xử lý đặc biệt (có thể cần thêm thư viện)
                        try:
                            img = Image.open(source_path)
                        except:
                            conversion_stats['skipped'] += 1
                            continue
                    else:
                        img = fix_image_rotation(source_path)
                    
                    # Convert sang RGB nếu cần
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Resize ảnh nếu quá lớn (giữ aspect ratio)
                    max_size = 1024
                    if max(img.size) > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
                    # Lưu ảnh
                    img.save(target_path, 'JPEG', quality=95)
                    
                    conversion_stats['converted'] += 1
                    conversion_stats[split_name] += 1
                    
                except Exception as e:
                    print(f"   ❌ Error processing {file}: {e}")
                    conversion_stats['errors'] += 1
    
    print(f"\n✅ Image conversion completed:")
    print(f"   Converted: {conversion_stats['converted']}")
    print(f"   Skipped: {conversion_stats['skipped']}")
    print(f"   Errors: {conversion_stats['errors']}")
    print(f"   Train: {conversion_stats['train']}")
    print(f"   Val: {conversion_stats['val']}")
    print(f"   Test: {conversion_stats['test']}")
    
    return class_names, class_mapping

def create_dataset_yaml(output_dir="vegetable_dataset", class_names=None):
    """Tạo file data.yaml cho YOLOv8"""
    print(f"\n📝 Creating dataset configuration...")
    
    if class_names is None:
        # Auto detect từ train folder
        train_dir = os.path.join(output_dir, 'train')
        class_names = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    
    # Tạo config
    config = {
        'path': os.path.abspath(output_dir),
        'train': 'train',
        'val': 'val',
        'test': 'test',
        'nc': len(class_names),  # number of classes
        'names': class_names
    }
    
    # Lưu file yaml
    yaml_path = os.path.join(output_dir, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    # Tạo class mapping JSON
    class_mapping = {name: idx for idx, name in enumerate(class_names)}
    json_path = os.path.join(output_dir, 'class_mapping.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(class_mapping, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {yaml_path}")
    print(f"✅ Created {json_path}")
    print(f"   Number of classes: {len(class_names)}")
    
    return yaml_path

def create_training_script(output_dir="vegetable_dataset"):
    """Tạo script training"""
    script_content = f'''# Training script cho Vegetable Classification
from ultralytics import YOLO
import torch

def train_vegetable_classifier():
    print("🥬 Training Vegetable Classification Model")
    print("=" * 50)
    
    # Check GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {{device}}")
    
    # Load model
    model = YOLO('yolov8n-cls.pt')  # Classification model
    
    # Training arguments
    args = {{
        'data': '{output_dir}',
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
    }}
    
    # Start training
    print("🚀 Starting training...")
    results = model.train(**args)
    
    print("\\n✅ Training completed!")
    print(f"Best model saved at: runs/classify/yolov8n_vegetables/weights/best.pt")
    
    # Validate
    print("\\n📊 Running validation...")
    metrics = model.val()
    print(f"Top-1 Accuracy: {{metrics.top1:.3f}}")
    print(f"Top-5 Accuracy: {{metrics.top5:.3f}}")
    
    return model, results

def test_model():
    """Test trained model"""
    print("\\n🧪 Testing model...")
    
    # Load best model
    model = YOLO('runs/classify/yolov8n_vegetables/weights/best.pt')
    
    # Test trên test set
    results = model.val(data='{output_dir}', split='test')
    print(f"Test Accuracy: {{results.top1:.3f}}")
    
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
    
    print(f"Prediction: {{class_name}} ({{confidence:.3f}})")
    return class_name, confidence

if __name__ == "__main__":
    # Train model
    model, results = train_vegetable_classifier()
    
    # Test model  
    test_results = test_model()
    
    print("\\n🎉 All done! Model ready for use.")
'''
    
    script_path = "train_vegetables.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Created training script: {script_path}")
    return script_path

def main():
    """Main function"""
    print("🥬 Vegetable Dataset Preparation for YOLOv8")
    print("=" * 60)
    
    # 1. Analyze dataset
    stats = analyze_dataset()
    
    # 2. Create YOLO structure
    output_dir = create_yolo_structure()
    
    # 3. Convert and organize images
    class_names, class_mapping = convert_and_copy_images()
    
    # 4. Create dataset YAML
    yaml_path = create_dataset_yaml(output_dir, class_names)
    
    # 5. Create training script
    script_path = create_training_script(output_dir)
    
    print(f"\\n🎉 Dataset preparation completed!")
    print(f"\\n📁 Output structure:")
    print(f"   {output_dir}/")
    print(f"   ├── train/           # Training images")
    print(f"   ├── val/             # Validation images") 
    print(f"   ├── test/            # Test images")
    print(f"   ├── data.yaml        # Dataset config")
    print(f"   └── class_mapping.json")
    print(f"\\n🚀 Next steps:")
    print(f"   1. python {script_path}")
    print(f"   2. Monitor training: tensorboard --logdir runs/classify")
    print(f"   3. Use trained model for prediction")
    
    return output_dir, class_names

if __name__ == "__main__":
    main()
