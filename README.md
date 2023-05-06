### QA through WA

This project is a demo to connect Whatsapp to using AI to respond based on company documents.

The project uses Langchain and openai api.

The inject script is inspired by the demo on hwchase17/notion-qa

## To use
recommend to use venv
```python -m venv venv```

Then activate the venv. using activate script. This process is different for Windows and Linux so refer to specific document.

```pip install -r requirements.txt```

please change .env-sample to .env after filling in the credentials.
then run 
```python main.py```

## Ingesting data
Place the unstructured data in md files under the report folder. Then run
```python ingest.py```