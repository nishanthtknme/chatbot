# chat/api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChatBotAPI(APIView):
    def post(self, request):
        user_message = request.data.get('message', '')
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Basic bot reply logic (replace with OpenAI or logic later)
        bot_reply = f"You said: {user_message}"

        return Response({'user': user_message, 'bot': bot_reply}, status=status.HTTP_200_OK)
