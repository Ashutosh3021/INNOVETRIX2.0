"""
SkillMatchAI - Run Script
Simple script to start the FastAPI application
Place this file in the root directory (BPUT folder)
"""
import uvicorn
import sys
from pathlib import Path

# Ensure we're in the correct directory
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting SkillMatchAI Server")
    print("=" * 60)
    print(f"📂 Root Directory: {root_dir}")
    print(f"🌐 API will be available at: http://localhost:8000")
    print(f"📚 Documentation at: http://localhost:8000/docs")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )