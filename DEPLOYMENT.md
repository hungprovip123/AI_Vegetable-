# 🚀 Deploy AI Web App - Hướng dẫn chi tiết

## 🥇 Railway (Khuyên dùng nhất!)

### Ưu điểm:
- ✅ $5 credit miễn phí/tháng 
- ✅ Không sleep như Heroku
- ✅ Auto-deploy từ GitHub
- ✅ Domain miễn phí

### Các bước:

1. **Push code lên GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Tạo tài khoản Railway**
   - Vào https://railway.app
   - Sign up với GitHub

3. **Deploy**
   - Click "New Project" 
   - Chọn "Deploy from GitHub repo"
   - Chọn repo của bạn
   - Railway sẽ tự động detect Python và deploy

4. **Environment Variables** (nếu cần)
   - Vào Settings > Environment
   - Thêm PORT=8000 (tự động)

---

## 🥈 Render

### Ưu điểm:
- ✅ Hoàn toàn miễn phí
- ✅ 750 giờ/tháng
- ❌ Sleep sau 15 phút không dùng

### Các bước:

1. **Push code lên GitHub** (như trên)

2. **Tạo tài khoản Render**
   - Vào https://render.com
   - Sign up với GitHub

3. **Deploy**
   - Click "New +" > "Web Service"
   - Connect GitHub repo
   - Name: vegetable-ai-app
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

---

## 🥉 Vercel (Serverless)

### Ưu điểm:
- ✅ Miễn phí tốt
- ✅ Domain đẹp
- ❌ Cần config serverless

### Các bước:

1. **Tạo vercel.json**
   ```json
   {
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

2. **Deploy**
   - Vào https://vercel.com
   - Import GitHub repo
   - Deploy!

---

## 📋 Checklist trước khi deploy:

- ✅ `railway.json` đã tạo
- ✅ `nixpacks.toml` đã tạo  
- ✅ `render.yaml` đã tạo
- ✅ `app.py` đã update PORT env var
- ✅ `requirements.txt` đầy đủ
- ✅ Model file có trong repo (hoặc download link)

## 🔧 Troubleshooting:

### Lỗi model không tìm thấy:
- Model quá lớn (>100MB) không thể push lên GitHub
- Giải pháp: Upload model lên Google Drive/Dropbox, download trong startup

### Lỗi memory:
- Free tier có giới hạn RAM
- Optimize model hoặc dùng plan trả phí

### Lỗi timeout:
- Free tier có giới hạn request time
- Optimize inference code

---

**Khuyến nghị: Bắt đầu với Railway, nếu không được thì dùng Render!**
