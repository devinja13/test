# REMS Scheduling Optimizer

This repository contains a React + TypeScript frontend built with Vite and a FastAPI backend.

## Frontend
The frontend project is located under `REMS-Scheduling-Optimizer-INFORMS/rems-model-web-app`.

### Install dependencies
```bash
cd REMS-Scheduling-Optimizer-INFORMS/rems-model-web-app
npm install
```

### Development server
```bash
npm run dev
```

### Production build
```bash
npm run build
```

## Backend
The Python backend can be run with `uvicorn`. Dependencies are defined in `pyproject.toml`.

```bash
cd REMS-Scheduling-Optimizer-INFORMS/rems-model-web-app/backend
pip install -e .
python main.py
```
