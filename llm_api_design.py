from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# Hugging Face API key
HF_API_KEY = "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"

# FastAPI app starting
app = FastAPI()

# Pydantic models
class TextRequest(BaseModel):
    text: str

class QuestionRequest(BaseModel):
    question: str
    context: str


@app.post("/generate/")
async def generate_text(request: TextRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": request.text}
    response = requests.post("https://api-inference.huggingface.co/models/gpt2", headers=headers, json=payload)
    
    # Check if the response status code is OK
    if response.status_code == 200:
        try:
            response_data = response.json()  # Attempt to parse the JSON response
            generated_text = response_data[0]['generated_text']
            return {"generated_text": generated_text}
        except ValueError:
            return {"error": "Error parsing JSON response from Hugging Face API"}
        except KeyError:
            return {"error": "'generated_text' key not found in the response"}
    else:
        # Handle cases where the API request failed
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}



@app.post("/summarize/")
async def summarize_text(request: TextRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": request.text}
    response = requests.post("https://api-inference.huggingface.co/models/facebook/bart-large-cnn", headers=headers, json=payload)
    summary = response.json()[0]['summary_text']
    return {"summary": summary}


@app.post("/qa/")
async def question_answer(request: QuestionRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": {"question": request.question, "context": request.context}}
    response = requests.post("https://api-inference.huggingface.co/models/deepset/roberta-base-squad2", headers=headers, json=payload)
    answer = response.json()['answer']
    return {"answer": answer}


#sentiment analysis
@app.post("/sentiment/")
async def sentiment_analysis(request: TextRequest):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": request.text}
    response = requests.post("https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english", headers=headers, json=payload)

    print("Raw API Response:", response.text)  # Yanıtı ekrana yazdır

    if response.status_code == 200:
        try:
            response_data = response.json()
            print("Response Data:", response_data)  # JSON formatını kontrol et

            if isinstance(response_data, list) and len(response_data) > 0 and isinstance(response_data[0], dict):
                label = response_data[0].get("label", "Unknown")
                score = response_data[0].get("score", 0.0)

                return {"sentiment": label, "confidence": score}
            else:
                return {"error": f"Unexpected response format: {response_data}"}
        except ValueError:
            return {"error": "Error parsing JSON response from Hugging Face API"}
    else:
        return {"error": f"Request failed with status code {response.status_code}", "details": response.text}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
