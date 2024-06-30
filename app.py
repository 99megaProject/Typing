import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI

load_dotenv()
api_key = os.environ.get('API_KEY')
app = FastAPI()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

@app.get('/api/v1/para')
def para(query:str, length:int=0):
    try:
        query_about = "Write down about {}".format(query)
        if length!=0 : query_about = query_about + ' more than {} words. '.format(length)
        response = model.generate_content(query_about)
        data = str(response.text)
        if response._done == False : raise Exception("Paragraph generation failed")
        return { 'message' : 'Paragraph generated successfully', 'status_code' : 200, 'data' : data}
    except Exception as e:
        return { 'message' : "Can't generate paragraph", 'status_code' : 400, 'error' : str(e)}

