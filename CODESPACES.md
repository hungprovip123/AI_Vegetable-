# 🚀 Deploy với GitHub Codespaces

## ✨ Ưu điểm GitHub Codespaces:
- ✅ **Miễn phí 60 giờ/tháng** 
- ✅ **Full Python environment** trong browser
- ✅ **Public URL** cho web app
- ✅ **Không cần setup local**
- ✅ **Auto-install dependencies**

## 🎯 Cách sử dụng:

### 1. Tạo Codespace:
1. Vào GitHub repo: https://github.com/hungprovip123/AI_Vegetable-
2. Click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
3. Đợi 2-3 phút để setup environment

### 2. Chạy App:
```bash
# Trong Codespace terminal:
python app.py
```

### 3. Access Web App:
- Codespace sẽ auto-forward port 8000
- Click **"Open in Browser"** khi popup hiện
- Hoặc vào **"Ports"** tab → click port 8000

### 4. Public URL:
- Trong **"Ports"** tab, right-click port 8000
- Chọn **"Port Visibility"** → **"Public"**
- Copy public URL để share

## 🔧 Tự động setup:

### `.devcontainer/devcontainer.json`:
- Auto-install Python 3.11
- Auto-install requirements.txt
- Auto-forward port 8000
- Setup VSCode extensions

### Model Download:
- App sẽ tự động download model từ Google Drive khi start
- Lần đầu chạy sẽ mất 1-2 phút download

## ⏱️ Giới hạn:
- **60 giờ/tháng** miễn phí
- **Sleep sau 30 phút** không hoạt động
- **2 core, 4GB RAM** (đủ cho AI app)

## 🎯 Perfect cho:
- ✅ **Demo/Test** web app
- ✅ **Development** không cần local setup
- ✅ **Share** với người khác
- ✅ **Prototype** AI projects

---

**GitHub Codespaces = Cloud IDE + Web Hosting miễn phí!** 🚀
