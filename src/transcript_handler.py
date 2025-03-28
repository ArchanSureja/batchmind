import nltk 
from logger import logger 
def load_transcript(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Transcript file not found : {file_path}")
        return None 
    except Exception as e:
        logger.error(f"Error reading Transcript file : {file_path}")
        return None 


""" 
Improvment : 
- semantic chunking can be used over simple sentence based chunking 
- finding natural break in text , using similarity score between two consecutive sentences 
- adjusting the chunk size to API's token limit 
"""
def perform_chunking(text, chunk_size_chars=1000,overlap_chars=100):
    sentences = nltk.sent_tokenize(text)
    if not sentences:
        return []
    chunks = []
    current_chunk = ""
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence) + 1 # 1 for white space
        if current_length + sentence_length > chunk_size_chars:
            chunks.append(current_chunk.strip())
            current_chunk = current_chunk[-overlap_chars:].strip() if overlap_chars > 0 else ""
            current_length = len(current_chunk)
        
        current_chunk += sentence + " "
        current_length += sentence_length
    if current_chunk:
        chunks.append(current_chunk.strip())
    logger.info(f"Total number of chunks created : {len(chunks)} ")
    return chunks 