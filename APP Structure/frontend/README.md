# Green Energy Trading Platform - Frontend

React-based frontend for the AI-powered Green Energy Trading Platform with real-time analytics and smart contract integration.

## 🚀 Features

- **Real-time Trading Dashboard** - Live updates via WebSocket
- **AI-Powered Predictions** - Price forecasting, demand analysis, trend detection
- **Smart Contract Integration** - Web3 wallet connection and contract execution
- **Interactive Analytics** - Charts and visualizations with Chart.js
- **Responsive Design** - Mobile-first, accessible UI
- **Dark Mode Support** - System preference + manual toggle

## 📦 Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite 5
- **State Management**: Zustand + React Context
- **Data Fetching**: Axios + React Query
- **Real-time**: Socket.io Client
- **Charts**: Chart.js + Recharts
- **Blockchain**: Web3.js
- **Styling**: CSS Variables (Design System)
- **Router**: React Router v6

## 🛠️ Installation

### Prerequisites

- Node.js 18+ and npm 9+
- Backend server running on port 5000

### Setup

```bash
# Navigate to frontend directory
cd green-energy-platform/frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start development server
npm run dev
