from fastapi import FastAPI
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")


@app.get("/")
async def root(input_text: str):
    processed = nlp(input_text)
    processed_dict = processed.to_json()
    return {"result": processed_dict}
