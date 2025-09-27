# 🚀 Deploy lên Google Cloud Platform

## ✨ Ưu điểm GCP:
- 💰 **$200 credit miễn phí** cho new users
- ⚡ **Cloud Run serverless** - chỉ trả khi có request  
- 🔄 **Auto-scale** 0 → 1000 instances
- 🌏 **Global CDN** tích hợp
- 📊 **Advanced monitoring** 

## 🎯 OPTION 1: CLOUD RUN (KHUYÊN DÙNG)

### Bước 1: Setup GCP
```bash
# Install Google Cloud SDK
# Windows: Download từ https://cloud.google.com/sdk/docs/install
# Mac: brew install --cask google-cloud-sdk
# Linux: curl https://sdk.cloud.google.com | bash

# Login và setup project
gcloud auth login
gcloud projects create vegetable-ai-project --name="Vietnamese Vegetable AI"
gcloud config set project vegetable-ai-project
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### Bước 2: Deploy với Cloud Build
```bash
# Submit build từ GitHub repo
gcloud builds submit --config cloudbuild.yaml

# Hoặc build manual
gcloud builds submit --tag gcr.io/vegetable-ai-project/vegetable-ai
gcloud run deploy vegetable-ai-app \
  --image gcr.io/vegetable-ai-project/vegetable-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 2Gi \
  --cpu 2
```

### Bước 3: Get Public URL
```bash
gcloud run services describe vegetable-ai-app --region us-central1
```

## 🔧 OPTION 2: APP ENGINE

### Deploy App Engine:
```bash
gcloud app create --region=us-central
gcloud app deploy app.yaml
gcloud app browse
```

## 💰 Cost Estimation với $200 Credit:

### Cloud Run:
- **Request**: $0.40 per 1M requests
- **CPU**: $0.00002400 per vCPU-second  
- **Memory**: $0.00000250 per GB-second
- **$200 = ~83M requests** hoặc **~8M CPU seconds**

### App Engine:
- **Instance hours**: ~$0.05 per hour
- **$200 = ~4000 hours** (~5.5 tháng 24/7)

## 🎯 Tính năng GCP:

### ✅ Cloud Run Features:
- **Concurrency**: 1000 requests per instance
- **Timeout**: 60 phút max
- **Memory**: 32GB max
- **CPU**: 8 vCPU max
- **Cold start**: ~1-2 giây

### ✅ Monitoring:
- **Cloud Logging**: Real-time logs
- **Cloud Monitoring**: Metrics & alerts  
- **Error Reporting**: Auto error tracking

### ✅ Security:
- **IAM**: Fine-grained permissions
- **VPC**: Private networking
- **SSL**: Auto HTTPS certificates

## 🚀 Advanced Setup:

### Custom Domain:
```bash
gcloud run domain-mappings create --service vegetable-ai-app --domain your-domain.com
```

### Environment Variables:
```bash
gcloud run services update vegetable-ai-app \
  --set-env-vars="MODEL_URL=https://drive.google.com/..."
```

### CI/CD với GitHub:
```bash
gcloud builds triggers create github \
  --repo-name=AI_Vegetable- \
  --repo-owner=hungprovip123 \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

---

## 📋 Checklist:

- [ ] Tạo GCP account + $200 credit
- [ ] Install Google Cloud SDK  
- [ ] Create project
- [ ] Enable APIs (Cloud Build, Cloud Run)
- [ ] Deploy với cloudbuild.yaml
- [ ] Test public URL
- [ ] Setup monitoring

**GCP = Enterprise-grade hosting với $200 credit!** 🚀
