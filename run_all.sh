#!/bin/bash

# Complete startup script for the anime website
# This script starts all services in the correct order

echo "============================================================"
echo "🚀 Starting Anime Website Application"
echo "============================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
echo -e "\n${BLUE}📊 Checking PostgreSQL...${NC}"
if docker ps | grep -q anime_postgres; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${BLUE}Starting PostgreSQL...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✓ PostgreSQL started${NC}"
    echo "Waiting 10 seconds for database to be ready..."
    sleep 10
fi

# Check if database is initialized
echo -e "\n${BLUE}🗄️  Checking database initialization...${NC}"
if docker exec anime_postgres psql -U anime_user -d anime_db -c "SELECT COUNT(*) FROM anime" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database is initialized${NC}"
else
    echo -e "${BLUE}Initializing database...${NC}"
    python database/init_db.py
fi

# Start backend in a new terminal/tmux session
echo -e "\n${BLUE}🔧 Starting Backend API...${NC}"
if command -v tmux &> /dev/null; then
    tmux new-session -d -s anime_backend "cd backend && source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate && pip install -q -r requirements.txt && python main.py"
    echo -e "${GREEN}✓ Backend started in tmux session 'anime_backend'${NC}"
else
    echo -e "${RED}⚠ tmux not found. Please start backend manually:${NC}"
    echo "  cd backend && source venv/bin/activate && python main.py"
fi

# Wait a moment for backend to start
sleep 3

# Start recommender in a new terminal/tmux session
echo -e "\n${BLUE}🤖 Starting Recommendation Service...${NC}"
if command -v tmux &> /dev/null; then
    tmux new-session -d -s anime_recommender "cd recommender && source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate && pip install -q -r requirements.txt && python main.py"
    echo -e "${GREEN}✓ Recommender started in tmux session 'anime_recommender'${NC}"
else
    echo -e "${RED}⚠ tmux not found. Please start recommender manually:${NC}"
    echo "  cd recommender && source venv/bin/activate && python main.py"
fi

# Wait a moment for recommender to start
sleep 3

# Start frontend in a new terminal/tmux session
echo -e "\n${BLUE}💻 Starting Frontend...${NC}"
if command -v tmux &> /dev/null; then
    tmux new-session -d -s anime_frontend "cd frontend && npm install --silent && npm run dev"
    echo -e "${GREEN}✓ Frontend started in tmux session 'anime_frontend'${NC}"
else
    echo -e "${RED}⚠ tmux not found. Please start frontend manually:${NC}"
    echo "  cd frontend && npm install && npm run dev"
fi

echo -e "\n============================================================"
echo -e "${GREEN}✅ All services started!${NC}"
echo "============================================================"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:    http://localhost:3000"
echo "   Backend API: http://localhost:8000/docs"
echo "   Recommender: http://localhost:8001/docs"
echo ""

if command -v tmux &> /dev/null; then
    echo "📺 View logs:"
    echo "   Backend:     tmux attach -t anime_backend"
    echo "   Recommender: tmux attach -t anime_recommender"
    echo "   Frontend:    tmux attach -t anime_frontend"
    echo ""
    echo "🛑 Stop all services:"
    echo "   tmux kill-session -t anime_backend"
    echo "   tmux kill-session -t anime_recommender"
    echo "   tmux kill-session -t anime_frontend"
    echo "   docker-compose down"
fi

echo ""
echo "============================================================"
