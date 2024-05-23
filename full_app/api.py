from langchain_community.llms.ollama import Ollama
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
# Initialize the Ollama model with the specified parameters and callback manager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
llama_llm = Ollama(model="llama3:8b-instruct-q8_0",callbacks=[StreamingStdOutCallbackHandler()])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""]
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI  named SocialPal that helps plan social events using local buisnesses, introduce yourself and ask questions one by one to help understand the users needs and always ask for specifications and use follow up questions.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ]
)

messages_sent_history = ChatMessageHistory()

chain = prompt | llama_llm

chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: messages_sent_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

@app.get("/")
def root():
    return {"message":"Api Working!"}

@app.get("/stream_chat/{message}")
async def send_message(message: str):
    print(message)
    stream  = chain_with_message_history.stream(
    {"input": message},
    {"configurable": {"session_id": "unused"}})
    return StreamingResponse(stream,media_type="text/event-stream")


