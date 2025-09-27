# 🥬 Vietnamese Vegetable Classification AI

Hệ thống nhận diện rau củ Việt Nam sử dụng AI với YOLOv8 và FastAPI.

## ✨ Tính năng

- 🤖 **AI nhận diện** 81 loại rau củ Việt Nam
- 🌐 **Web interface** thân thiện
- 📡 **REST API** đầy đủ
- 🎯 **Độ chính xác cao** với YOLOv8
- 📱 **Responsive design** 
- 🚀 **Deploy sẵn** trên Railway/Render

## 🎯 Demo

### Web Interface
![Web Interface](static/images/demo-web.png)

### API Documentation
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🚀 Cài đặt và chạy

### 1. Clone repository
```bash
git clone https://github.com/hungprovip123/AI_Vegetable-.git
cd AI_Vegetable-
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
python app.py
```

Truy cập: http://localhost:8000

## 📁 Cấu trúc project

```
AI_Vegetable-/
├── app.py                          # FastAPI main application
├── requirements.txt                # Python dependencies
├── static/                         # Static files
│   ├── css/style.css              # Styles
│   └── js/app.js                  # JavaScript
├── templates/                      # HTML templates
│   ├── index.html                 # Main page
│   └── about.html                 # About page
├── vegetable_classification/       # Trained model
│   └── yolov8n_vegetables/
│       └── weights/best.pt        # YOLOv8 model
├── vegetable_dataset/             # Training dataset
├── prepare_vegetable_dataset.py   # Dataset preparation
├── train_vegetables.py            # Training script
├── test_vegetable_model.py        # Testing script
└── run_server.py                  # Development server

# Deployment configs
├── railway.json                   # Railway config
├── nixpacks.toml                 # Railway build config
├── render.yaml                   # Render config
├── Dockerfile                    # Docker config
└── docker-compose.yml           # Docker Compose
```

## 🎯 API Endpoints

### Prediction
- `POST /api/predict` - Dự đoán từ file upload
- `POST /api/predict-url` - Dự đoán từ URL

### Utility
- `GET /api/health` - Health check
- `GET /api/model-info` - Thông tin model
- `GET /api/classes` - Danh sách classes

## 🧠 AI Model

- **Architecture**: YOLOv8n Classification
- **Classes**: 81 loại rau củ Việt Nam
- **Accuracy**: ~95% trên test set
- **Input**: Images (JPG, PNG, WebP)
- **Output**: Class prediction + confidence

### Supported Vegetables
Bao gồm: Bầu, Bí, Cà chua, Cà tím, Cà rót, Dưa leo, Đậu, Hành, Khoai, Nấm, Ớt, Rau muống, v.v...

## 🚀 Deployment

### Railway (Khuyên dùng)
1. Fork repo này
2. Vào https://railway.app
3. "New Project" → "Deploy from GitHub"
4. Chọn repo → Auto deploy!

### Render
1. Fork repo này  
2. Vào https://render.com
3. "New Web Service" → Connect repo
4. Build: `pip install -r requirements.txt`
5. Start: `python app.py`

### Docker
```bash
docker-compose up --build
```

## 🛠️ Development

### Training custom model
```bash
python prepare_vegetable_dataset.py  # Prepare dataset
python train_vegetables.py           # Train model
python test_vegetable_model.py       # Test model
```

### Development server
```bash
python run_server.py  # With health checks
```

## 📊 Performance

- **Inference time**: ~200ms per image
- **Model size**: ~6MB
- **Memory usage**: ~200MB
- **Supported formats**: JPG, PNG, WebP
- **Max file size**: 10MB

## 🤝 Contribute

1. Fork repo
2. Tạo feature branch: `git checkout -b feature/new-feature`
3. Commit: `git commit -m 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Tạo Pull Request

## 📄 License

MIT License - xem [LICENSE](LICENSE) file.

## 🙏 Credits

- **YOLOv8**: Ultralytics
- **FastAPI**: Sebastián Ramirez
- **Dataset**: Vietnamese vegetables collection
- **Icons**: FontAwesome

## 📞 Liên hệ

- GitHub: [@hungprovip123](https://github.com/hungprovip123)
- Project: [AI_Vegetable-](https://github.com/hungprovip123/AI_Vegetable-)

---

**Made with ❤️ for Vietnamese agriculture**
