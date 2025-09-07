#!/usr/bin/env python3
"""
Development startup script for Agent Mira
Starts the backend server and provides helpful commands
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_docker():
    """Check if Docker is running"""
    success, _, _ = run_command("docker --version")
    if not success:
        print("❌ Docker is not installed or not running")
        return False
    
    success, _, _ = run_command("docker-compose --version")
    if not success:
        print("❌ Docker Compose is not installed")
        return False
    
    print("✅ Docker and Docker Compose are available")
    return True

def start_services():
    """Start all services using Docker Compose"""
    print("🚀 Starting Agent Mira services...")
    
    # Check if services are already running
    success, _, _ = run_command("docker-compose ps -q")
    if success and _.strip():
        print("⚠️  Services are already running. Stopping first...")
        run_command("docker-compose down")
    
    # Start services
    success, stdout, stderr = run_command("docker-compose up -d")
    if not success:
        print(f"❌ Failed to start services: {stderr}")
        return False
    
    print("✅ Services started successfully!")
    return True

def wait_for_services():
    """Wait for services to be ready"""
    print("⏳ Waiting for services to be ready...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            # Check backend health
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                break
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    else:
        print("❌ Services failed to start within expected time")
        return False
    
    return True

def seed_database():
    """Seed the database with sample data"""
    print("🌱 Seeding database with sample data...")
    
    success, stdout, stderr = run_command(
        "docker-compose exec backend python seed_data.py"
    )
    
    if success:
        print("✅ Database seeded successfully!")
    else:
        print(f"⚠️  Database seeding failed: {stderr}")
        print("   You can manually seed the database later with:")
        print("   docker-compose exec backend python seed_data.py")

def show_status():
    """Show service status and URLs"""
    print("\n" + "="*50)
    print("🎉 Agent Mira is ready!")
    print("="*50)
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n📋 Useful commands:")
    print("   View logs: docker-compose logs -f")
    print("   Stop services: docker-compose down")
    print("   Restart: docker-compose restart")
    print("   Shell access: docker-compose exec backend bash")
    print("="*50)

def main():
    """Main startup function"""
    print("🏗️  Agent Mira - Property Recommendation System")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("docker-compose.yml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("\n💡 Please install Docker and Docker Compose first:")
        print("   https://docs.docker.com/get-docker/")
        sys.exit(1)
    
    # Start services
    if not start_services():
        sys.exit(1)
    
    # Wait for services
    if not wait_for_services():
        print("❌ Services failed to start properly")
        print("   Check logs with: docker-compose logs")
        sys.exit(1)
    
    # Seed database
    seed_database()
    
    # Show status
    show_status()

if __name__ == "__main__":
    main()
