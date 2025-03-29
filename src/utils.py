from logger import logger
import json 


def load_questions(file_path):
    """ load questions from questions.json"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Questions file not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from questions file: {file_path}")
        return []
    

def write_response(file_path,results,questions,):
    """ write response to the data/response.txt"""
    try:
        with open(file_path, 'w') as f:
            f.write("\n--- Batch Prediction Results ---\n")
            for question_id, answer in results:
                question_data = next((q for q in questions if q.get('id') == question_id or q.get('question') == question_id), None)
                question_text = question_data.get('question') if question_data else f"ID: {question_id}"
                f.write(f"\nQuestion ({question_id}): {question_text}\n")
                if answer:
                    f.write(f"Answer: {answer}\n")
                else:
                    f.write("Answer not found or error occurred.\n")
    except Exception as e:
        logger.error(f"Error writing response to file: {e}")
