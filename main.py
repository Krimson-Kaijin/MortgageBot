from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    try:
        print("📩 User message:", chat.message)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful mortgage assistant for Assurant Home Loans."},
                {"role": "user", "content": chat.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        gpt_reply = response.choices[0].message.content
        print("💬 GPT reply:", gpt_reply)
        return {"response": gpt_reply}

    except Exception as e:
        print("❌ ERROR calling GPT:", e)
        return {
            "response": "Sorry, something went wrong. Please try again soon or contact support.",
            "error": str(e)
        }

@app.get("/")
def home():
    return {"message": "Mortgagebot is live 🚀"}
