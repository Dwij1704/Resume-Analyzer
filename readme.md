# Resume Analyzer

## 📝 Overview

Resume Analyzer is an AI-powered web application that analyzes resumes against job descriptions. It provides a rating, identifies matching keywords, and offers feedback to help job seekers improve their resumes.

## 🚀 Features

- 📄 Upload and analyze PDF resumes
- 💼 Compare resumes against custom job descriptions
- 🤖 AI-powered analysis using OpenAI's GPT model
- ⭐ Receive a rating out of 10 for resume-job description match
- 🔑 Identify top matching keywords
- 💡 Get personalized feedback for resume improvement
- 📚 Save and manage job description presets
- 🌓 Dark mode for comfortable viewing
- 📱 Responsive design for desktop and mobile use

## 🛠️ Technology Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- AI: OpenAI GPT-3.5 Turbo
- PDF Processing: PyPDF2
- Styling: Bootstrap 5

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key

## 🔧 Setup

1. Clone the repository:
   ```
   git clone https://github.com/Dwij1704/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Initialize the job description presets file:
   ```
   echo "[]" > job_description_presets.txt
   ```

### 🐳 Docker Setup

1. Build the Docker image:
   ```
   docker build -t healthcare-ai-chatbot .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 -e OPENAI_API_KEY=your_openai_api_key_here 
   healthcare-ai-chatbot
   ```

3. Open a web browser and navigate to `http://localhost:5000`

## 🚀 Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

## 💻 Usage

1. Upload a PDF resume using the file input.
2. Enter a job description in the text area or select a preset from the sidebar.
3. Click "Analyze Resume" to start the analysis.
4. View the results, including the rating, matching keywords, and feedback.
5. Use the "Add New Preset" button to save frequently used job descriptions.

## 🌙 Dark Mode

Toggle dark mode by clicking the "Toggle Dark Mode" button in the top right corner.

## 📁 Project Structure

```
Resume-Analyzer/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this file)
├── job_description_presets.txt  # Saved job description presets
├── uploads/                # Temporary folder for uploaded resumes
└── templates/
    └── index.html          # Main HTML template
```

## 🛠️ Customization

- To add or modify initial job description presets, edit the `job_description_presets.txt` file.
- Adjust the AI prompt or analysis criteria in the `/analyze` route in `app.py`.
- Modify the UI by editing the HTML and CSS in `templates/index.html`.

## ⚠️ Limitations

- The application uses the OpenAI API, which may incur costs based on usage.
- PDF parsing may not be perfect for all resume formats.
- The AI analysis is based on the GPT-3.5 Turbo model and may not always provide perfect results.