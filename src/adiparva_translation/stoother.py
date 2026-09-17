import json
from ollama import Client
import time

client = Client(
    host="http://localhost:11434",
    timeout=1800
)

MODEL = "qwen3:8b"
 
def translate(sanskrit_text, language):
    
    start = time.perf_counter()
    language_names = {
        "hindi": "Hindi",
        "english": "English",
        "nepali": "Nepali",
    }

    target_language_name = language_names.get(
        language.lower(),
        language
    )

    prompt = f"""
You are a Sanskrit translator.

Translate the following Sanskrit text from Sanskrit into {target_language_name}.

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{ 
  "{language}": "..."
}}

Rules:
- Translate the Sanskrit meaning accurately into {target_language_name}.
- Do not translate the reference.
- Do not add explanations.
- Do not add comments.
- Do not use Markdown.
- Return valid JSON.
- Do not add any additional fields.

Sanskrit text:
{sanskrit_text}
"""

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    content = response["message"]["content"].strip()
    elapsed = time.perf_counter() - start
    print(f"Time taken: {elapsed:.2f} seconds")
    return json.loads(content)


sanskrit_text = "\n".join([
    "आदौ मङ्गलाचरणं",
    "नैमिशारण्ये दीर्घसत्रे शौनकादीन्प्रति सौतेरागमनम्",
    "तत्र शौनकादिभिः सौतिं प्रति भारतकथनचोदना",
    "सौतिना श्रीमन्नारायणनमस्कारपूर्वकं व्यासस्य भारतनिर्माणकथनम्",
    "पर्वानुक्रमणिका",
])

result = translate(
    sanskrit_text,
    "hindi"
)

print(json.dumps(result, ensure_ascii=False, indent=2))
