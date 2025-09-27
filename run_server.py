#!/usr/bin/env python3
"""
Vietnamese Vegetable Classification - Development Server
Run this script to start the development server
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import ultralytics
        import PIL
        import cv2
        import numpy
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return False

def check_model():
    """Check if trained model exists"""
    model_paths = [
        'vegetable_classification/yolov8n_vegetables/weights/best.pt',
        'runs/classify/yolov8n_vegetables/weights/best.pt'
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"✅ Found trained model: {path}")
            return True
    
    print("❌ No trained model found!")
    print("🔧 Please train the model first: python train_vegetables.py")
    return False

def check_dataset():
    """Check if dataset exists"""
    if os.path.exists('vegetable_dataset/data.yaml'):
        print("✅ Dataset configuration found")
        return True
    else:
        print("❌ Dataset not found!")
        print("🔧 Please prepare dataset first: python prepare_vegetable_dataset.py")
        return False

def check_directories():
    """Check and create necessary directories"""
    dirs = ['static/css', 'static/js', 'static/images', 'templates']
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory structure verified")
    return True

def start_server():
    """Start the development server"""
    print("🚀 Starting Vietnamese Vegetable Classification Server...")
    print("="*60)
    print("📱 Web Interface: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("📊 Health Check: http://localhost:8000/api/health")
    print("="*60)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Run uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

def main():
    """Main function"""
    print("🥬 Vietnamese Vegetable Classification - Development Server")
    print("="*60)
    
    # Check all requirements
    checks = [
        ("Requirements", check_requirements),
        ("Dataset", check_dataset), 
        ("Model", check_model),
        ("Directories", check_directories),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
            print(f"❌ {name} check failed")
            break
        print(f"✅ {name} check passed")
    
    if all_passed:
        print("\n✅ All checks passed! Starting server...")
        start_server()
    else:
        print("\n❌ Please fix the issues above before starting the server")
        sys.exit(1)

if __name__ == "__main__":
    main()
