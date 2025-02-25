import os
from dotenv import load_dotenv
import PyPDF2
import google.generativeai as genai  # Import the Gemini API library

# Load environment variables from .env file
load_dotenv()

def calculate_score(file_path):
    """
    Extracts text from the uploaded PDF and calls the Gemini API to calculate a resume score.
    Returns the score as an integer (1-10) or None if there's an error.
    """
    # Step 1: Extract text from PDF using PyPDF2 (same as before - good part!)
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None  # Return None to indicate failure

    if not text: # Check if text extraction actually resulted in text
        print("No text extracted from PDF.")
        return None

    # Step 2: Get the Gemini API key and Configure Gemini API
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Gemini API key not set in environment variables (GEMINI_API_KEY).")
        return None

    genai.configure(api_key=gemini_api_key) # Configure Gemini API with the key
    model = genai.GenerativeModel('gemini-pro') # Use 'gemini-pro' model


    # Step 3: Prepare the prompt for Gemini API -  Crucial for getting score!
    prompt_text = f"""
    Evaluate the following resume text and provide a score from 1 to 10,
    where 10 is an excellent resume and 1 is a very poor resume.
    Focus on clarity, conciseness, ATS freindlyness, relevance to typical job requirements,
    and overall presentation. 
    Also keep in mind that the text you're about to evaluate is converted from a PDF file via PyPDF2. So there might be inconsistencies.
    Be harsh but fair.
    Just return the score as a single integer number, no explanation needed.
    Under no circumstances you may return a text response. Just the score. If the text is not a resume, return 0.

    Resume Text:
    {text}
    """

    # Step 4: Call the Gemini API using the google-generativeai library
    try:
        response = model.generate_content(prompt_text)
        score_text = response.text.strip()

        try:
            score = int(score_text)
            if 1 <= score <= 10:
                return score
            else:
                print(f"Gemini returned score out of range: {score}")
                return None # Indicate invalid score range
        except ValueError:
            print(f"Gemini returned non-numeric score: {score_text}")
            return None # Indicate non-numeric score
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None # Indicate API call error

def calculate_review(file_path):
    """
    Extracts text from the uploaded PDF and calls the Gemini API to provide a basic resume review,
    assess ATS friendliness, and suggest improvements.
    Returns a dictionary containing the review, ATS friendliness assessment, and improvement suggestions,
    or None if there's an error.  Score is omitted in this function.
    """
    # Step 1: Extract text from PDF using PyPDF2 (same as before)
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None  # Return None to indicate failure

    if not text: # Check if text extraction actually resulted in text
        print("No text extracted from PDF.")
        return None

    # Step 2: Get the Gemini API key and Configure Gemini API
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Gemini API key not set in environment variables (GEMINI_API_KEY).")
        return None

    genai.configure(api_key=gemini_api_key) # Configure Gemini API with the key
    model = genai.GenerativeModel('gemini-pro') # Use 'gemini-pro' model


    # Step 3: Prepare the PROMPT for Gemini API - Modified to request ONLY review and suggestions (NO SCORE)
    prompt_text = f"""
    You are a Resume anaylisis AI. Your task is to evaluate the following resume text and provide a review of the content, with data-driven insights and personalized improvement tips.
    Evaluate the following resume text and provide a review of the content,
    focusing on ATS friendliness, clarity, and relevance to typical job requirements.
    Your response should be constructive and provide suggestions for improvement.
    Also keep in mind that the text you're about to evaluate is converted from a PDF file via PyPDF2. So there might be inconsistencies in formatting so omit them.
    The response will be only simple plaintext. No bullet points or complex formatting needed.
    Response length limit is 100 words.
    
    Resume Text:
    {text}
    """

    # Step 4: Call the Gemini API using the google-generativeai library
    try:
        response = model.generate_content(prompt_text)
        full_response_text = response.text.strip()
        return full_response_text
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None # Indicate API call error