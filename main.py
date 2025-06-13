from fastapi import FastAPI, Depends, HTTPException
from models import LoginRequest
from auth import authenticate_user, create_access_token, get_current_user
from memory import append_user_message, get_user_context, clear_user_context
from openai import OpenAI
import os
from dotenv import load_dotenv
from models import ChatRequest
from fastapi import status



app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mortgagebot is live 🚀"}



app = FastAPI()

@app.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}



app = FastAPI()


@app.get("/")
def home():
    return {"message": "Mortgagebot is live 🚀"}


@app.post("/login")
def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Welcome back, {user}!"}



@app.get("/test-memory")
def test_chat_memory(user_id: str = Depends(get_current_user)):
    append_user_message(user_id, "user", "Hello from test route")
    return get_user_context(user_id)


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest, user_id: str = Depends(get_current_user)):
    try:
        # Add user's message to memory
        append_user_message(user_id, "user", chat.message)

        # Fetch context for the current user
        context = get_user_context(user_id)

        # Prepend system message to the chat
        context_with_system = [
            {"role": "system",
             "content": "You are a helpful assistant for Assurant Home Loans. You specialize in helping customers with Mortgage applications and pre-approval processes,Home loan products (conventional, FHA, VA, USDA loans), Interest rates and payment calculations, Refinancing options, Down payment assistance programs, Credit requirements and improvement tips, Home buying process guidance, Loan documentation requirements. Always be professional, helpful, and provide accurate information about home loans and mortgages. If you don't know specific current rates or policies, advise the customer to contact Assurant directly for the most up-to-date information."}] + context

        # Send to GPT-3.5
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context_with_system,
            max_tokens=300,
            temperature=0.7
        )

        # Get GPT's reply
        gpt_reply = response.choices[0].message.content.strip()

        # Add assistant reply to memory
        append_user_message(user_id, "assistant", gpt_reply)

        return {"response": gpt_reply}

    except Exception as e:
        return {"response": "Something went wrong", "error": str(e)}

@app.get("/history")
def get_chat_history(user_id: str = Depends(get_current_user)):
    return get_user_context(user_id)



@app.post("/reset", status_code=status.HTTP_200_OK)
def reset_chat(user_id: str = Depends(get_current_user)):
    clear_user_context(user_id)
    return {"message": f"Chat history cleared for {user_id}."}

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "OK",
        "message": "Mortgagebot is running",
        "version": "1.0.0"
    }
"""load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev/testing — restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        }"""

