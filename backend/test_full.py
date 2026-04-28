import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("Testing API Key...")
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key found: {bool(api_key)}")
if api_key:
    print(f"API Key length: {len(api_key)}")
    print(f"API Key (first 20 chars): {api_key[:20]}")

print("\nTesting AI service import...")
try:
    from ai_service import get_ai_service
    print("AI service imported successfully")
    
    service = get_ai_service()
    print(f"Service created: {service is not None}")
    
    if service:
        print("Testing threat analysis...")
        result = service.analyze_threat(50, 50, 50, "https://example.com/track")
        print("Result:", result)
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()