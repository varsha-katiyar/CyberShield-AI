import requests

# Test AI recommendations endpoint
try:
    response = requests.post('http://localhost:5000/ai/recommendations', json={
        'threat_level': 'medium',
        'threat_details': {'score': 50, 'status': 'Suspicious'}
    })
    print("AI Recommendations Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)

# Test AI assess-url endpoint
try:
    response = requests.post('http://localhost:5000/ai/assess-url', json={
        'url': 'https://example.com'
    })
    print("\nAI URL Assessment Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)