# chat_view.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama runs on this by default

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Call local LLaMA 3 via Ollama
        try:
            response = requests.post(OLLAMA_API_URL, json={
                "model": "llama3",
                "prompt": user_message,
                "stream": False
            })
            response.raise_for_status()
            result = response.json()
            return JsonResponse({"reply": result.get("response", "No reply")})
        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request"}, status=400)
