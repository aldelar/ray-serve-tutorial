import dotenv, os

from starlette.requests import Request

import ray
from ray import serve

from transformers import pipeline

# showcase use of ENV variables (.env would be in gitignore for a real project)
from dotenv import load_dotenv
load_dotenv()
VAR_1 = os.environ["VAR_1"]
VAR_2 = os.environ["VAR_2"]

@serve.deployment
class Translator:

    def __init__(self):
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)
        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]
        return translation

@serve.deployment
class Summarizer:
    
    def __init__(self, translator):
        # Load model
        self.model = pipeline("summarization", model="t5-small")
        self.translator = translator

    def summarize(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5, max_length=15)
        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]
        return summary

    async def __call__(self, http_request: Request) -> str:
        english_text: str = await http_request.json()
        summary = self.summarize(english_text)
        print(summary)
        translation_ref = await self.translator.translate.remote(summary)
        translation = await translation_ref
        return translation

deployment_graph = Summarizer.bind(Translator.bind())