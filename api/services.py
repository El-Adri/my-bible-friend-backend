import google.generativeai as genai
from django.conf import settings


class GeminiConfigurationError(Exception):
    pass


class GeminiServiceError(Exception):
    pass


class GeminiService:
    model_name = "gemini-3.1-flash-lite-preview"

    def __init__(self) -> None:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise GeminiConfigurationError(
                "La variable d'environnement GEMINI_API_KEY est manquante."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
        except Exception as exc:  # pragma: no cover - depend d'un service externe
            raise GeminiServiceError(
                "Echec lors de l'appel a Gemini. Verifie la cle API ou la connectivite."
            ) from exc

        text = (getattr(response, "text", None) or "").strip()
        if not text:
            raise GeminiServiceError("Gemini a retourne une reponse vide.")

        return text

