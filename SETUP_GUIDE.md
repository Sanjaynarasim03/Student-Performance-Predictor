# 🚀 Setup & Deployment Guide - Student Performance Predictor

Complete guide for setting up the Student Performance Predictor application locally and deploying to various platforms.

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8 or higher**
  ```bash
  python --version
  ```
- **Node.js 14 or higher** (for React frontend)
  ```bash
  node --version
  npm --version
  ```
- **Git**
  ```bash
  git --version
  ```

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/student-performance-predictor.git
cd student-performance-predictor
```

### Step 2: Backend Setup (Flask API)

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -c "import flask, pandas, sklearn; print('All packages installed successfully')"
   ```

4. **Start the Flask Server**
   ```bash
   python app.py
   ```
   
   The API will be available at: `http://localhost:5000`

5. **Test the API**
   ```bash
   curl http://localhost:5000/
   ```

### Step 3: Frontend Setup

#### Option A: HTML Version (Recommended for beginners)

1. **Simply open in browser**
   ```bash
   # Open index.html in your preferred browser
   open index.html  # macOS
   start index.html # Windows
   xdg-open index.html # Linux
   ```

2. **Or use a simple HTTP server**
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Then visit http://localhost:8000
   ```

#### Option B: React Version (Advanced)

1. **Navigate to React Directory**
   ```bash
   mkdir -p frontend/react-version/src/components
   cd frontend/react-version
   ```

2. **Initialize React App** (if not already done)
   ```bash
   npx create-react-app . --template=minimal
   ```

3. **Install Dependencies**
   ```bash
   npm install
   ```

4. **Copy React Files**
   ```bash
   # Copy the provided React files to appropriate locations:
   # - App.js → src/App.js
   # - App.css → src/App.css
   # - StudentForm.js → src/components/StudentForm.js
   # - StudentForm.css → src/components/StudentForm.css
   # - PredictionResult.js → src/components/PredictionResult.js
   # - PredictionResult.css → src/components/PredictionResult.css
   ```

5. **Start React Development Server**
   ```bash
   npm start
   ```
   
   The React app will be available at: `http://localhost:3000`

### Step 4: Verify Complete Setup

1. **Check Backend**: Visit `http://localhost:5000` - should return API status
2. **Check Frontend**: Visit your frontend URL - should display the form
3. **Test Integration**: Submit the form - should return prediction results

---

## Docker Deployment

### Prerequisites
- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)

### Step 1: Create Docker Configuration

#### Dockerfile (Backend)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - .:/app
  
  frontend:
    image: nginx:alpine
    ports:
      - "3000:80"
    volumes:
      - ./index.html:/usr/share/nginx/html/index.html:ro
    depends_on:
      - backend
```

### Step 2: Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 3: Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

---

## Production Deployment

### Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account created

#### Step 1: Prepare for Heroku

1. **Create Procfile**
   ```text
   web: gunicorn app:app
   ```

2. **Update requirements.txt**
   ```text
   Flask==2.3.3
   Flask-CORS==4.0.0
   pandas==2.1.1
   numpy==1.24.3
   scikit-learn==1.3.0
   joblib==1.3.2
   gunicorn==20.1.0
   ```

3. **Create runtime.txt**
   ```text
   python-3.9.18
   ```

#### Step 2: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### AWS EC2 Deployment

#### Step 1: Launch EC2 Instance

1. Launch Ubuntu 22.04 LTS instance
2. Configure security group (ports 22, 80, 443, 5000)
3. Connect via SSH

#### Step 2: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/student-performance-predictor.git
cd student-performance-predictor

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install and configure Gunicorn
pip install gunicorn

# Test Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

#### Step 3: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/student-predictor
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/student-predictor /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 4: Create Systemd Service

```bash
sudo nano /etc/systemd/system/student-predictor.service
```

Add service configuration:
```ini
[Unit]
Description=Student Performance Predictor
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/student-performance-predictor
Environment="PATH=/home/ubuntu/student-performance-predictor/venv/bin"
ExecStart=/home/ubuntu/student-performance-predictor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start student-predictor
sudo systemctl enable student-predictor
sudo systemctl status student-predictor
```

### Google Cloud Platform Deployment

#### Step 1: Setup GCP Project

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Create new project
gcloud projects create your-project-id
gcloud config set project your-project-id
```

#### Step 2: Deploy with App Engine

1. **Create app.yaml**
   ```yaml
   runtime: python39
   
   env_variables:
     FLASK_ENV: production
   
   handlers:
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   gcloud app browse
   ```

---

## Environment Variables

### Development
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
```

### Production
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

---

## Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. CORS errors in browser
- Ensure Flask-CORS is installed: `pip install Flask-CORS`
- Check that CORS is configured in app.py
- Try running backend on different port

#### 3. Port already in use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### 4. React build issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 5. Model loading errors
- Ensure model files are in the correct directory
- Check file permissions
- Verify scikit-learn version compatibility

### Performance Optimization

#### Backend Optimization
```python
# Add to app.py for production
if __name__ == '__main__':
    app.run(debug=False, threaded=True, port=5000)
```

#### Frontend Optimization
```bash
# Build React for production
npm run build

# Serve static files with nginx
sudo cp -r build/* /var/www/html/
```

### Monitoring and Logging

#### Add Logging to Flask App
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add to routes
@app.route('/predict', methods=['POST'])
def predict():
    logger.info('Prediction request received')
    # ... existing code
```

#### Monitor with PM2 (Alternative to systemd)
```bash
npm install -g pm2
pm2 start app.py --name student-predictor --interpreter python3
pm2 startup
pm2 save
```

---

## Security Considerations

### For Production Deployment

1. **Environment Variables**: Never commit API keys or sensitive data
2. **CORS Configuration**: Restrict origins to your domain
3. **Input Validation**: Validate all user inputs
4. **HTTPS**: Use SSL certificates (Let's Encrypt recommended)
5. **Rate Limiting**: Implement rate limiting to prevent abuse

### Example Security Enhancements

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict():
    # ... existing code
```

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review error logs
3. Create an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version, etc.)

---

## Next Steps

After successful deployment:

1. **Add Monitoring**: Implement logging and monitoring
2. **Set up CI/CD**: Automate testing and deployment
3. **Scale**: Consider load balancing for high traffic
4. **Backup**: Implement regular data backups
5. **Updates**: Plan for regular security updates

For more information, see the main [README.md](README.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md).