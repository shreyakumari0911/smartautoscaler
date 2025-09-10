# Smart Cloud Autoscaler 🚀

An intelligent cloud resource autoscaler that uses machine learning to predict system load and make scaling decisions. This project demonstrates a complete cloud-native application with monitoring, ML-based predictions, and automated scaling.

## 🌟 Features

- Real-time system metrics monitoring (CPU, Memory)
- ML-based load prediction using Scikit-learn
- Automated scaling decisions based on predictions
- Beautiful real-time dashboard with React + Tailwind
- Prometheus + Grafana monitoring stack
- CI/CD pipeline with GitHub Actions
- Containerized deployment with Docker

## 🏗️ Project Structure

```
smartscaling/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── model.py          # ML model training
│   │   ├── predict.py        # Prediction logic
│   │   ├── metrics.py        # Prometheus metrics
│   │   └── autoscaler.py     # Scaling logic
│   ├── tests/
│   │   └── test_backend.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_backend.sh
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MetricsChart.jsx
│   │   │   └── ScalingStatus.jsx
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       └── dashboards/
│           └── autoscaler.json
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docker-compose.yml
├── render.yaml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose
- Git

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/shreyakumari0911/smartscaling.git
   cd smartscaling
   ```

2. Start the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Start monitoring stack:
   ```bash
   docker-compose up -d prometheus grafana
   ```

### Deployment

The application is configured for deployment on free-tier services:

- Backend API: Deployed on Render
- Frontend: Deployed on Vercel
- Monitoring: Prometheus + Grafana

## 📊 Monitoring Setup

1. Access Prometheus: http://localhost:9090
2. Access Grafana: http://localhost:3000 (default credentials: admin/admin)
3. Import the provided dashboard from `monitoring/grafana/dashboards/autoscaler.json`

## 🔄 CI/CD Pipeline

The project includes GitHub Actions workflows that:
- Run tests on pull requests
- Deploy to Render on push to main
- Build and deploy frontend to Vercel

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Key endpoints:
- `GET /metrics`: Prometheus metrics
- `GET /predict`: Get load predictions
- `GET /status`: Current scaling status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - feel free to use this project for learning and development purposes.

## 🙏 Acknowledgments

- FastAPI for the backend framework
- Scikit-learn for ML capabilities
- React + Tailwind for the frontend
- Prometheus + Grafana for monitoring
- Render and Vercel for hosting 
