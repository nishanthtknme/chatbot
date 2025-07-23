# assistant/urls.py
from django.urls import path
from assistant.views.chatbot import chatbot_page, chatbot_response
from assistant.views.chatbot import chatbot_page, chatbot_response, chat_history

urlpatterns = [
    path('', chatbot_page, name='chat-page'),
    path('api/chat/', chatbot_response, name='chatbot-response'),
    path('chat-history/', chat_history, name='chat_history_html'),


]
