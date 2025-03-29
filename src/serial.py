from utils import load_questions , write_response
from config import get_api_key 
from logger import logger
from transcript_handler import load_transcript
from google import genai 
import asyncio
import time 
def generate_answer(client,context,question):
    prompt = f"{context}\n\nQuestion: {question}"
    response = client.models.generate_content(
        model='gemini-2.0-flash',contents={prompt}

    )
    return response.text
def main():
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    questions = load_questions("data/questions.json")
    transcript = load_transcript("data/transcript.txt")
    results = []
    for index,question in enumerate(questions):
    
        question_id = question.get('id',question.get('question'))
        question_text = question.get('question')
        logger.info(f"Processing question {index+1}/{len(questions)}: {question_id}")
        answer = generate_answer(client=client,context=transcript,question=question_text)
        results.append((question_id,answer)) 
        time.sleep(4)
    write_response("data/serial_response.txt",results,questions=questions)

if __name__ == "__main__":
    main()