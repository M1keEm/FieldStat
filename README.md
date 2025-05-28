# FieldStat

FieldStat is a web-based platform for agricultural data analysis and visualization. It enables users to collect, analyze, and visualize field and weather data to support decision-making in crop management.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Backend (Flask)](#backend-flask)
- [Frontend (React)](#frontend-react)
- [Development](#development)
- [License](#license)

## Features
- User authentication and authorization
- Data collection and management for agricultural fields
- Weather data integration
- Interactive dashboards and charts
- RESTful API backend
- Modern, responsive frontend UI

## Architecture
FieldStat consists of two main components:
- **Backend:** Python Flask API for data processing, authentication, and business logic
- **Frontend:** React application for user interaction and data visualization

Both components are containerized using Docker and orchestrated with Docker Compose.

## Getting Started
### Prerequisites
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/)

### Quick Start
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FieldStat
   ```
2. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access the frontend at `http://localhost:3000` and the backend API at `http://localhost:5000`.

## Backend (Flask)
- Located in the `backendFlask/` directory
- Main entry point: `app.py`
- Configuration: `config.py`
- API routes: `routes/`
- Services: `services/`
- Tests: `tests/`
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Frontend (React)
- Located in the `frontendReact/` directory
- Main entry point: `src/main.jsx`
- Components: `src/components/`
- Install dependencies:
  ```bash
  npm install
  ```
- Start development server:
  ```bash
  npm run dev
  ```

## Development
- Use Docker Compose for full-stack development and testing
- Backend and frontend can be developed and tested independently
- Run tests for backend:
  ```bash
  cd backendFlask
  pytest
  ```

## License
This project is licensed under the MIT License.

