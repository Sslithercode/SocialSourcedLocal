from flask import Flask, redirect, url_for, render_template, request
import asyncio


from langchain_community.llms.ollama import Ollama
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_together import ChatTogether
# choose from our 50+ models here: https://docs.together.ai/docs/inference-models
#llama_llm = ChatTogether(
    #together_api_key="",
    #model="meta-llama/Llama-3-8b-chat-hf",
    #streaming = True
#)


#llama_llm = Ollama(model="llama3:8b-instruct-q8_0",callbacks=[StreamingStdOutCallbackHandler()])
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

app = Flask(__name__)
app.secret_key = "hello"

messages = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/planning", methods=["POST", "GET"])
def interact():
    if request.method == "POST":
        user_input = request.form["userInput"]
        messages.append(user_input)
        stream  = chain_with_message_history.invoke( {"input": user_input},{"configurable": {"session_id": "unused"}})
        messages.append(stream.content)
        
        #for i in stream:
            #messages[-1] += i
            #print(i)
        
        return render_template("interact.html", data=messages)
    else:
        return render_template("interact.html", data=messages)



@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/clean_list', methods=['POST'])
def clean_list():
    global messages
    messages = []
    return redirect(url_for("interact"))

if __name__ == "__main__":
    app.run(debug=True)