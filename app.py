import os
import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['PRESETS_FILE'] = 'job_description_presets.txt'

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files or 'jobDescription' not in request.form:
        return jsonify({"error": "Missing resume file or job description"}), 400

    file = request.files['resume']
    job_description = request.form['jobDescription']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            resume_text = extract_text_from_pdf(file_path)

            prompt = f"""
            Analyze the following resume against the job description. 
            Rate the resume on a scale of 1-10 and identify the top 5 matching keywords.

            Resume:
            {resume_text[:2000]}  # Limiting to first 2000 characters

            Job Description:
            {job_description[:1000]}  # Limiting to first 1000 characters

            Provide the output in the following JSON format:
            {{
                "rating": <1-10 rating>,
                "matching_keywords": [<list of top 5 matching keywords>],
                "feedback": <brief explanation of the rating and suggestions for improvement>
            }}
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant skilled in resume analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )
                
                analysis = response.choices[0].message.content

                # Parse the JSON string returned by the AI
                parsed_analysis = json.loads(analysis)
                
                # Return the parsed JSON directly
                return jsonify(parsed_analysis)

            except json.JSONDecodeError:
                # If parsing fails, return the raw response
                return jsonify({
                    "error": "Failed to parse AI response as JSON",
                    "raw_response": analysis
                })

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        finally:
            os.remove(file_path)  # Clean up the uploaded file

    return jsonify({"error": "Invalid file type"}), 400
@app.route('/get_presets', methods=['GET'])
def get_presets():
    try:
        with open(app.config['PRESETS_FILE'], 'r') as file:
            presets = json.load(file)
        return jsonify(presets)
    except FileNotFoundError:
        return jsonify([])

@app.route('/add_preset', methods=['POST'])
def add_preset():
    new_preset = request.json
    try:
        with open(app.config['PRESETS_FILE'], 'r') as file:
            presets = json.load(file)
    except FileNotFoundError:
        presets = []
    
    presets.append(new_preset)
    
    with open(app.config['PRESETS_FILE'], 'w') as file:
        json.dump(presets, file, indent=2)
    
    return jsonify({"success": True})

def initialize_app():
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        logger.info(f"Uploads folder created/verified: {app.config['UPLOAD_FOLDER']}")
    except Exception as e:
        logger.error(f"Failed to create uploads folder: {e}")
    
    # Create presets file if it doesn't exist
    if not os.path.exists(app.config['PRESETS_FILE']):
        try:
            with open(app.config['PRESETS_FILE'], 'w') as file:
                json.dump([], file)
            logger.info(f"Presets file created: {app.config['PRESETS_FILE']}")
        except Exception as e:
            logger.error(f"Failed to create presets file: {e}")
    
if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)