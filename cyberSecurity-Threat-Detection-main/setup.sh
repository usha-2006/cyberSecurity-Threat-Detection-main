#!/bin/bash

# Cybersecurity Threat Detection System Setup Script
# This script sets up the development environment and dependencies

set -e

echo "=========================================="
echo "Cybersecurity Threat Detection System Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
    echo "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p models

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOL
# Threat Detection System Environment Variables
ENVIRONMENT=development
LOG_LEVEL=INFO

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Database Configuration
ELASTICSEARCH_HOSTS=http://localhost:9200
MONGODB_URI=mongodb://localhost:27017
REDIS_HOST=localhost

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security Configuration
JWT_SECRET=your-super-secret-jwt-key-change-in-production
ENCRYPTION_KEY=your-encryption-key-change-in-production
EOL
    echo ".env file created. Please review and update the secrets."
fi

# Download sample threat intelligence data
echo "Downloading sample threat intelligence..."
if [ ! -d "data/threat_intel" ]; then
    mkdir -p data/threat_intel
    # This would typically download from threat intelligence feeds
    echo "Sample threat intelligence data would be downloaded here"
fi

# Set up test data
echo "Setting up test data..."
if [ ! -f "data/test_samples.json" ]; then
    cat > data/test_samples.json << EOL
[
  {
    "type": "network_traffic",
    "source_ip": "192.168.1.100",
    "dest_ip": "malicious-site.com",
    "protocol": "TCP",
    "timestamp": "2024-01-01T10:00:00Z"
  },
  {
    "type": "auth_log",
    "event": "failed_login",
    "user": "admin",
    "attempts": 5,
    "timestamp": "2024-01-01T10:01:00Z"
  },
  {
    "type": "web_traffic",
    "url": "legitimate-site.com/about",
    "referrer": "google.com",
    "timestamp": "2024-01-01T10:02:00Z"
  }
]
EOL
fi

# Make scripts executable
chmod +x test_system.py

echo ""
echo "Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Review and update the .env file with your configuration"
echo "2. Start the required services: docker-compose up -d"
echo "3. Run tests: python test_system.py"
echo "4. Start the API: python src/api/main.py"
echo ""
echo "For production deployment:"
echo "- Update config/production.yaml"
echo "- Set proper secrets in .env"
echo "- Use Docker Compose: docker-compose -f docker-compose.yml up -d"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
