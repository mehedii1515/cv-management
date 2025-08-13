#!/bin/bash
# Resume Parser Search System - Production Startup
# Usage: ./start_system.sh [port]

PORT=${1:-8000}

echo "🚀 Starting Resume Parser Search System on port $PORT"
echo "============================================"

# Check if Elasticsearch is running
if ! curl -s "localhost:9200" > /dev/null 2>&1; then
    echo "⚠️  Elasticsearch not detected on localhost:9200"
    echo "   Please start Elasticsearch first"
    echo "   Windows: Run elasticsearch.bat from Elasticsearch installation"
    echo "   Linux/Mac: systemctl start elasticsearch"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the system
echo "Starting Django API server..."
python manage.py runserver 0.0.0.0:$PORT --noreload &
DJANGO_PID=$!

echo "✅ System started!"
echo ""
echo "📊 API Endpoints:"
echo "   Status:     http://localhost:$PORT/api/search/status/"
echo "   Search:     http://localhost:$PORT/api/search/search/?q=python"
echo "   Boolean:    http://localhost:$PORT/api/search/boolean-search/?q=python%20AND%20django"
echo "   Suggestions: http://localhost:$PORT/api/search/suggestions/?q=prog"
echo ""
echo "🔍 Test the system:"
echo "   curl 'http://localhost:$PORT/api/search/search/?q=python'"
echo ""
echo "🛑 To stop the system:"
echo "   kill $DJANGO_PID"
echo ""
echo "📊 Monitor integration:"
echo "   python monitor_integration.py"
echo ""

# Keep script running
trap "echo ''; echo '🛑 Stopping system...'; kill $DJANGO_PID 2>/dev/null; exit 0" INT TERM

echo "System running... Press Ctrl+C to stop"
while kill -0 $DJANGO_PID 2>/dev/null; do
    sleep 1
done

echo "System stopped."
