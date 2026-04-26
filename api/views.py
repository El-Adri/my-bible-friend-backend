from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .prompts import (
    ADVICE_PROMPT_TEMPLATE,
    CHAT_PROMPT_TEMPLATE,
    STORY_PROMPT_TEMPLATE,
    build_prompt,
)
from .serializers import AIResponseSerializer, UserMessageSerializer
from .services import GeminiConfigurationError, GeminiService, GeminiServiceError


class BaseGeminiView(APIView):
    prompt_template = ""

    def post(self, request):
        serializer = UserMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_message = serializer.validated_data["message"]
        prompt = build_prompt(self.prompt_template, user_message)

        try:
            response_text = GeminiService().generate(prompt)
        except GeminiConfigurationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except GeminiServiceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response({"response": response_text}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["My Bible Friend"],
    summary="Questions bibliques",
    description="Repond a une question biblique de maniere claire, simple et basee sur la Bible.",
    request=UserMessageSerializer,
    responses={200: AIResponseSerializer},
    examples=[
        OpenApiExample(
            "Exemple chat",
            value={"message": "Pourquoi Dieu permet la souffrance ?"},
            request_only=True,
        )
    ],
)
class ChatView(BaseGeminiView):
    prompt_template = CHAT_PROMPT_TEMPLATE


@extend_schema(
    tags=["My Bible Friend"],
    summary="Conseils spirituels",
    description="Apporte un conseil spirituel empathique avec une base biblique.",
    request=UserMessageSerializer,
    responses={200: AIResponseSerializer},
    examples=[
        OpenApiExample(
            "Exemple advice",
            value={"message": "Je me sens triste et seul en ce moment."},
            request_only=True,
        )
    ],
)
class AdviceView(BaseGeminiView):
    prompt_template = ADVICE_PROMPT_TEMPLATE


@extend_schema(
    tags=["My Bible Friend"],
    summary="Histoires bibliques",
    description="Raconte une histoire biblique immersive avec une lecon spirituelle.",
    request=UserMessageSerializer,
    responses={200: AIResponseSerializer},
    examples=[
        OpenApiExample(
            "Exemple story",
            value={"message": "Raconte-moi l'histoire de David et Goliath."},
            request_only=True,
        )
    ],
)
class StoryView(BaseGeminiView):
    prompt_template = STORY_PROMPT_TEMPLATE

