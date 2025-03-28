from logger import logger 

"""
Simple KeyWord based questions matching 
Improvements 
- Using Sematic matching 
"""
def match_question_to_chunks(questions,chunks):
    question_chunk_mapping = {} 
    for i,chunk in enumerate(chunks):
        for question_data in questions:
            question = question_data.get('question')
            question_id = question_data.get('id',question)
            if question and any(kw.lower() in chunk.lower() for kw in question.lower().split()):
                if question_id not in question_chunk_mapping:
                    question_chunk_mapping[question_id] = []
                if i not in question_chunk_mapping[question_id]:
                    question_chunk_mapping[question_id].append(i)
    return question_chunk_mapping