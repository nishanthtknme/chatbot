# # assistant/views/chatbot.py
# from django.http import JsonResponse
# from django.shortcuts import render
# import ollama
# import re

# def chatbot_page(request):
#     return render(request, 'index.html')



# def format_numbered_list(text):
   
#     formatted = re.sub(r'\s*(\d\.)', r'\n\1', text)
#     return formatted.strip()

# def chatbot_response(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)
#         user_input = data.get('message', '')

#         response = ollama.chat(model='llama3', messages=[
#             {"role": "user", "content": user_input}
#         ])
#         raw_text = response['message']['content']
#         clean_text = raw_text.replace('**', '')
#         formatted_text = format_numbered_list(clean_text)

#         return JsonResponse({'response': formatted_text})

# assistant/views/chatbot.py
from django.http import JsonResponse
from django.shortcuts import render
from assistant.models import ChatMessage
import ollama
import re
import json
import requests
import os
from dotenv import load_dotenv
from django.conf import settings


load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
def chatbot_page(request):
    return render(request, 'index.html')

# def get_live_data_from_web(query):
#     headers = {"X-API-KEY": "your_serper_api_key"}
#     params = {"q": query}
#     response = requests.get("https://google.serper.dev/search", headers=headers, params=params)
#     data = response.json()
    
#     # Try getting snippet from first result
#     if data.get("organic"):
#         return data["organic"][0].get("snippet", "No result found.")
#     return "No result found."

def format_numbered_list(text):
    # Add newline before each number (1., 2., etc.)
    formatted = re.sub(r'\s*(\d\.)', r'\n\1', text)
    return formatted.strip()

# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message', '')

#         # Save user's message
#         ChatMessage.objects.create(role='user', message=user_input)

#         # Generate response from Ollama
#         response = ollama.chat(model='llama3', messages=[
#             {"role": "user", "content": user_input}
#         ])
#         raw_text = response['message']['content']
#         clean_text = raw_text.replace('**', '')
#         formatted_text = format_numbered_list(clean_text)

#         # Save bot's message
#         ChatMessage.objects.create(role='bot', message=formatted_text)

#         return JsonResponse({'response': formatted_text})


# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message', '')

#         # Optionally fetch live info
#         live_info = get_live_data_from_web(user_input)

#         # Combine user query + live data
#         prompt = f"{user_input}\n\nLive info:\n{live_info}"

#         response = ollama.chat(model='llama3', messages=[
#             {"role": "user", "content": prompt}
#         ])

#         raw_text = response['message']['content']
#         clean_text = raw_text.replace('**', '')
#         formatted_text = format_numbered_list(clean_text)

#         return JsonResponse({'response': formatted_text})


# def get_live_data_from_serper(query):
#     headers = {
#         "X-API-KEY": SERPER_API_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {
#         "q": query
#     }
#     try:
#         response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
#         results = response.json()
#         if "organic" in results and len(results["organic"]) > 0:
#             top_result = results["organic"][0]
#             return f"{top_result['title']}\n{top_result['link']}\n{top_result['snippet']}"
#         else:
#             return "No relevant information found."
#     except Exception as e:
#         return f"Error fetching live data: {str(e)}"


def get_live_data_from_serper(query):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "q": query
    }
    try:
        response = requests.post("https://google.serper.dev/news", headers=headers, json=data)
        results = response.json()
        if "news" in results and len(results["news"]) > 0:
            snippets = []
            for article in results["news"][:3]:  # Top 3 articles
                snippet = f"{article['title']}\n{article['link']}\n{article['snippet']}"
                snippets.append(snippet)
            return "\n\n".join(snippets)
        else:
            return "No relevant news found."
    except Exception as e:
        return f"Error fetching news: {str(e)}"




# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message', '')

#         ChatMessage.objects.create(role='user', message=user_input)

#         live_data = get_live_data_from_serper(user_input)
#         print("Live data used in prompt:", live_data)  # Debug

#         if "No relevant information" in live_data or "Error" in live_data:
#             prompt = f"User question: {user_input}"
#         else:
#             prompt = f"User question: {user_input}\n\nHere is some live information to help answer:\n{live_data}"

#         response = ollama.chat(model='llama3', messages=[
#             {"role": "user", "content": prompt}
#         ])

#         raw_text = response['message']['content']
#         clean_text = raw_text.replace('**', '')
#         formatted_text = format_numbered_list(clean_text)

#         ChatMessage.objects.create(role='bot', message=formatted_text)

#         return JsonResponse({
#             'response': formatted_text,
#             'live_data': live_data  # Optional for frontend
#         })

def chatbot_response(request):
    if request.method == "POST":
        user_input = json.loads(request.body).get("message", "").strip()

        # Optional: save user's input to DB
        ChatMessage.objects.create(role='user', message=user_input)

        # 🔍 Use Serper for specific real-time queries
        if "2024 cricket world cup" in user_input.lower() or "who won" in user_input.lower():
            search_data = {
                "q": "2024 T20 Cricket World Cup winner site:icc-cricket.com"
            }

            headers = {
                "X-API-KEY": settings.SERPER_API_KEY,
                "Content-Type": "application/json"
            }

            try:
                res = requests.post("https://google.serper.dev/search", headers=headers, json=search_data)
                if res.status_code == 200:
                    result = res.json()
                    if result.get("organic"):
                        snippet = result["organic"][0].get("snippet", "No information available.")
                        response_text = snippet
                    else:
                        response_text = "Sorry, I couldn’t find up-to-date info right now."
                else:
                    response_text = "Error fetching live data."
            except Exception as e:
                response_text = f"Failed to fetch from web: {str(e)}"

            # Save bot reply
            ChatMessage.objects.create(role='bot', message=response_text)
            return JsonResponse({"response": response_text})

        # 🤖 Use Ollama for everything else
        try:
            response = ollama.chat(model='llama3', messages=[
                {"role": "user", "content": user_input}
            ])
            raw_text = response['message']['content']
            clean_text = raw_text.replace('**', '')
            formatted_text = format_numbered_list(clean_text)

            # Save response
            ChatMessage.objects.create(role='bot', message=formatted_text)

            return JsonResponse({'response': formatted_text})
        except Exception as e:
            return JsonResponse({'response': f"Ollama failed: {str(e)}"})


    
def chat_history(request):
    messages = ChatMessage.objects.order_by("timestamp")
    return render(request, 'chat_history.html', {'messages': messages})