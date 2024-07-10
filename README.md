# Django-Slack-RAG-bot

# Sytstem Design [Slack] Bot RAG

This project is a Slack bot integrated with a Retrieval-Augmented Generation (RAG) with knowledge of system design to assist users by providing explanations and attaching relevant images from a system design PDF [Alex Xu].



## Technologies Used
![App Screenshot](https://raw.githubusercontent.com/salam59/Django-Slack-RAG-bot/main/src/data/readme_images/IMG_20240710_100710.jpg)

### Backend
- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **Cloudflare Tunnels**: A tool to securely expose your local server to the internet.

### Retrieval-Augmented Generation (RAG) Technologies
- **Mistral AI**: An advanced AI model used for generating high-quality text.
- **jina.ai**: An Embedding model for vectorising the retrieved data
- **MongoDB**: A NoSQL database used for efficient storage, retrieval of data vector indexing.
- **pdfminer.six**: A Python library used to extract information from PDF documents.

### Additional Tools
- **Slack Bot**: A bot integrated with Slack to interact with users and provide responses.


## Roadmap
**Overall Flow:**

![App Screenshot](https://raw.githubusercontent.com/salam59/Django-Slack-RAG-bot/main/src/data/readme_images/IMG_20240709_200249.jpg)

**Data Processing:**

![App Screenshot](https://raw.githubusercontent.com/salam59/Django-Slack-RAG-bot/main/src/data/readme_images/IMG_20240709_195823.jpg)

**RAG Flow:**

![App Screenshot](https://raw.githubusercontent.com/salam59/Django-Slack-RAG-bot/main/src/data/readme_images/IMG20240709195859.jpg)


## Demo

![App Screenshot](https://raw.githubusercontent.com/salam59/Django-Slack-RAG-bot/main/src/data/readme_images/output.png)
## Project Setup
### Installation

Make sure to use environment

```bash
    python -m venv [name]
    source venv/bin/activate
```
Install project requirements
```bash
    python -m pip install -r requirements.txt
```
    
### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

    `SLACK_BOT_TOKEN`

    `DJANGO_SECRET_KEY`

    `CELERY_BROKER_URL`

    `CELERY_RESULT_BACKEND`

    `OPENAI_API_KEY`

    `MISTRAL_API_KEY`

    `HUGGING_FACE_KEY`

    `MONGO_USER` `MONGO_PASSWORD`

    `JINA_EMBEDDING`




### Deployment

To deploy this project run

```bash
python manage.py runserver 8177
```


## References to follow

For slack integration refer:

```bash
    https://api.slack.com/methods/files.getUploadURLExternal
    https://api.slack.com/methods/files.completeUploadExternal
```

For free embeddings:

```bash
    https://jina.ai/embeddings/
```

For Mongo Vector Index Setup:

```bash
   {
        "fields": [
            {
            "numDimensions": 768,
            "path": "[YOUR INDEX FIELD]",
            "similarity": "cosine",
            "type": "vector"
            }
        ]
    }
```
```bash
    https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-type/
```

```bash
    https://github.com/DataTalksClub/llm-zoomcamp
```

## Challenges Faced:
  - Data Processing from PDF [Alex Xu System Design]
  - Uploading an Image to Slack
    - we need to use 2 different APIs to upload a file. 
    - Refer to the references I have mentioned
    