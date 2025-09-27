#!/usr/bin/env python3
"""
Download model script for deployment
Model sẽ được download từ Google Drive khi deploy
"""

import os
import urllib.request
import zipfile
from pathlib import Path

def download_class_mapping():
    """Download class mapping từ Google Drive"""
    
    # Tạo thư mục nếu chưa có
    dataset_dir = Path("vegetable_dataset")
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    mapping_path = dataset_dir / "class_mapping.json"
    
    # Nếu mapping đã có thì skip
    if mapping_path.exists():
        print(f"✅ Class mapping already exists at {mapping_path}")
        return True
    
    print("📥 Downloading class mapping from Google Drive...")
    
    try:
        # Google Drive direct download link cho class mapping
        download_url = "https://drive.google.com/uc?export=download&id=1JlSySiIy8Ichh79MHaqwIiRAG8Mb1JXS"
        
        print(f"📡 Downloading from: {download_url}")
        urllib.request.urlretrieve(download_url, mapping_path)
        print(f"\n✅ Class mapping downloaded to {mapping_path}")
        
        # Verify file
        if mapping_path.stat().st_size > 100:  # At least 100 bytes
            print(f"✅ Class mapping verification successful ({mapping_path.stat().st_size} bytes)")
            return True
        else:
            print("❌ Downloaded class mapping seems too small")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading class mapping: {e}")
        return False

def download_model():
    """Download model từ Google Drive"""
    
    # Tạo thư mục nếu chưa có
    model_dir = Path("vegetable_classification/yolov8n_vegetables/weights")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / "best.pt"
    
    # Nếu model đã có thì skip
    if model_path.exists():
        print(f"✅ Model already exists at {model_path}")
        return True
    
    print("📥 Downloading model from Google Drive...")
    
    try:
        # URL Google Drive (cần update với link thật)
        # Cách tạo direct download link từ Google Drive:
        # 1. Upload model lên Google Drive
        # 2. Get sharing link: https://drive.google.com/file/d/FILE_ID/view?usp=sharing  
        # 3. Convert to direct link: https://drive.google.com/uc?export=download&id=FILE_ID
        
        # Google Drive direct download link cho model
        download_url = "https://drive.google.com/uc?export=download&id=1hw4JUHJWz2qFAvRKDWLtTNizeLiJj3NU"
        
        print(f"📡 Downloading from: {download_url}")
        
        # Download với progress
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, downloaded * 100 / total_size)
                print(f"\r⬇️  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
        
        urllib.request.urlretrieve(download_url, model_path, progress_hook)
        print(f"\n✅ Model downloaded to {model_path}")
        
        # Verify file size
        if model_path.stat().st_size > 1000:  # At least 1KB
            print(f"✅ Model verification successful ({model_path.stat().st_size} bytes)")
            return True
        else:
            print("❌ Downloaded file seems too small")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("💡 Please upload model manually or check the download URL")
        return False

def create_dummy_model():
    """Tạo dummy model để test deployment"""
    model_dir = Path("vegetable_classification/yolov8n_vegetables/weights") 
    model_dir.mkdir(parents=True, exist_ok=True)
    
    dummy_path = model_dir / "dummy.txt"
    with open(dummy_path, 'w') as f:
        f.write("Dummy model placeholder - replace with real model during deployment")
    
    print(f"✅ Created dummy model at {dummy_path}")

def download_all():
    """Download both model and class mapping"""
    print("🤖 Downloading Model & Class Mapping")
    print("=" * 50)
    
    # Download class mapping first (smaller file)
    mapping_success = download_class_mapping()
    
    # Download model
    model_success = download_model()
    
    if model_success and mapping_success:
        print("\n🎉 All files downloaded successfully!")
        return True
    elif model_success:
        print("\n⚠️ Model downloaded, but class mapping failed")
        return True
    else:
        print("\n❌ Model download failed")
        return False

if __name__ == "__main__":
    print("🤖 Model Download Script")
    print("=" * 50)
    
    success = download_all()
    
    if not success:
        print("\n🔧 Creating dummy model for testing...")
        create_dummy_model()
        print("\n📋 Files should be available at:")
        print("1. Model: vegetable_classification/yolov8n_vegetables/weights/best.pt")
        print("2. Class mapping: vegetable_dataset/class_mapping.json")
