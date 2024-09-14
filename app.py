from flask import Flask, render_template, request
import threading
import openai
import os
from resumeParser import extract_text_from_pdf

app = Flask(__name__)

# Lock for managing concurrency
lock = threading.Lock()

# For Open AI
# Function to call OpenAI API and process the resume
def process_resume(api_key, pdf_text, result):
    openai.api_key = api_key

    # Construct the prompt for generating HTML from resume text
    prompt = f"Convert the following resume text into a structured HTML format: {pdf_text}"

    try:
        # Using the ChatCompletion API with the `gpt-3.5-turbo` model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the updated model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000
        )

        # To extract and store the generated HTML in the result
        with lock:
            result["html_content"] = response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        with lock:
            result["html_content"] = f"Error processing resume: {e}"


            result["html_content"] = f"Error processing resume: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdfFile' not in request.files:
        return "No file uploaded", 400

    pdf_file = request.files['pdfFile']
    api_key = request.form['apiKey']

    if not pdf_file or not api_key:
        return "Missing file or API key", 400

    # To save the PDF file temporarily
    pdf_path = os.path.join("uploads", pdf_file.filename)
    pdf_file.save(pdf_path)

    # To extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Data structure to hold the result
    result = {}

    # To start a thread to process resume in the background
    thread = threading.Thread(target=process_resume, args=(api_key, pdf_text, result))
    thread.start()
    thread.join()

    # To pass the generated HTML resume to the frontend
    return render_template('result.html', resume_content=result.get("html_content", ""))

if __name__ == '__main__':
    app.run(debug=True)
    
 
 
    
# For Hugging Face 
# import requests

# def process_resume(api_key, pdf_text, result):
#     url = "https://api-inference.huggingface.co/models/gpt2"
#     headers = {"Authorization": f"Bearer {api_key}"}

#     data = {
#         "inputs": f"Generate a well-structured HTML resume from the following text: {pdf_text}"

#         #"inputs": f"Convert the following resume text into a structured HTML format: {pdf_text}",
#     }

#     try:
#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()
#         generated_text = response.json()[0]['generated_text']

#         with lock:
#             result["html_content"] = generated_text
#     except Exception as e:
#         print(f"Error processing resume: {e}")
#         with lock:
