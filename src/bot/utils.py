from openai import OpenAI
import helpers, requests, json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from pymongo import MongoClient

def get_openai_client():
    return OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key=helpers.config("OPENAI_API_KEY", default=None, cast=str),
        # 'ollama',
    )
def get_mongo_client():
    MONGO_USER = helpers.config("MONGO_USER", default=None, cast=str)
    MONGO_PASSWORD = helpers.config("MONGO_PASSWORD", default=None, cast=str)
    return MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@system-design.3tsw599.mongodb.net/?retryWrites=true&w=majority")

def generate_emebedding(message):
    url = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_KEY = helpers.config("JINA_EMBEDDING", default=None, cast=str)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_EMBEDDING_KEY}"
    }
    payload = {
        "model": "jina-clip-v1",
        "embedding_type": "float",
        "input": [
            {"text": message},
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        return response.text
    
def get_mongo_data(message):
    mongo_client = get_mongo_client()
    db = mongo_client["sys_design_data"]  
    collection = db["topics"] 

    pipeline = [
        {
            '$vectorSearch': {
            'index': 'rag_bot', 
            'path': 'content_embedding', 
            'queryVector': generate_emebedding(message),
            'numCandidates': 23, 
            'limit': 1
            }
        }, {
            '$project': {
                'Topic': 1, 
                'content': 1,
                'image_url': 1
            }
        }
    ]
    try:
        return collection.aggregate(pipeline)
    except Exception as e:
        print(f"Error in aggregation: {e}")
        return []


context_template = """
Topic: {Topic}
content: {content}
""".strip()

prompt_template = """
You're a system design expert teacher. Answer the QUESTION based on the CONTEXT provided.
Use only the facts from the CONTEXT when answering the QUESTION. If there are any questions in the context ignore the questions 
and consider other parts of the content. Also give output point-wise so that it is easy to understand, make the points short and easy to understand..

QUESTION: {question}

CONTEXT:
{context}
""".strip()


def build_context(documents):
    context_result = ""
    # breakpoint()
    documents = list(documents)
    print(len(documents))
    image_url = documents[0]["image_url"]
    topic = documents[0]["Topic"]
    for doc in documents:
        doc_str = context_template.format(Topic=doc["Topic"], content=doc["content"])
        context_result += ("\n\n" + doc_str)
    
    return context_result.strip(), image_url, topic


def build_prompt(user_question):
    documents = get_mongo_data(user_question)
    context, image_url, topic = build_context(documents=documents)
    prompt = prompt_template.format(
        question=user_question,
        context=context
    )
    return prompt, image_url, topic


def query_rag(message, raw=False):
    client = get_openai_client()
    # response = client.chat.completions.create(
    #     model='phi3',
    #     messages=[{"role": "user", "content": message}],
    # )
    response, image_url = run_mistral(message)
    if raw:
        return response, image_url
    return response, image_url

def run_mistral(user_message, model="mistral-medium-latest"):
    image_url = ""
    try:
        client = MistralClient(api_key=helpers.config("MISTRAL_API_KEY", default=None, cast=str))
        prompt, image_url, topic = build_prompt(user_message)
        messages = [
            ChatMessage(role="user", content=prompt)
        ]
        chat_response = client.chat(
            model=model,
            messages=messages
        )
        return f"{topic}\n\n{chat_response.choices[0].message.content}", image_url
    except Exception as e:
        print(f"Error running mistral: {e}")
        return "", image_url

