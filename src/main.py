import asyncio

from utils import load_questions , write_response
from config import get_api_key,get_max_concurrent_requests 
from logger import logger
from transcript_handler import load_transcript, perform_chunking
from question_matcher import match_question_to_chunks
from google import genai
import redis 
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
async def async_cache_get(key):
    value = await asyncio.to_thread(redis_client.get, key)
    return value

async def async_cache_set(key, value, expiration=3600):
    await asyncio.to_thread(redis_client.setex, key, expiration, value)
   

async def generate_answer(client, context, question):
    global api_calls
    prompt = f"{context}\n\nQuestion: {question}"
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents={prompt}
        )
        api_calls+=1
        if response and response.text:
            return response.text
        return None
    except Exception as e:
        logger.error(f"API error : {e}")
        return None

async def process_question(client, question_data, relevant_chunks,chunks,rate_limiter):
    global cache_hit    
    question_id = question_data.get('id', question_data.get('question'))
    question_text = question_data.get('question')
    if not question_text or not relevant_chunks:
        return question_id, None
    
    for chunk_index in relevant_chunks:
        chunk = chunks[chunk_index]
        cache_key = f"{question_text[:30]}_{chunk_index}"
        cached_ans = await async_cache_get(cache_key)

        if cached_ans:

            return question_id, cached_ans
        
        lock_key = f"lock:{cache_key}"
        lock_set = await asyncio.to_thread(redis_client.setnx,lock_key,"LOCKED")

        if lock_set:
            await asyncio.to_thread(redis_client.expire,lock_key,30)

            async with rate_limiter:
                logger.info(f"Calling API for '{question_text[:30]}...' with chunk {chunk_index}.")
                answer = await generate_answer(client,chunk,question_text)
                logger.info(f"Response from API for '{question_text[:30]}...")

            if answer:
                await async_cache_set(cache_key,answer)
                await asyncio.to_thread(redis_client.delete,lock_key)
                return question_id, answer
        else:
            while not cached_ans:
                await asyncio.sleep(0.5)
                cached_ans = await async_cache_get(cache_key)

            return question_id,cached_ans
    return question_id, None

async def main():
    logger.info("Starting main app...")
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)
    
    transcript = load_transcript("data/transcript.txt")
    questions = load_questions("data/questions.json")

    chunks = perform_chunking(transcript)
    question_chunk_mapping = match_question_to_chunks(questions,chunks)
    tasks = [] 
    rate_limiter = asyncio.Semaphore(get_max_concurrent_requests())
    global api_calls 
    api_calls = 0

    for question_data in questions:
        question_id = question_data.get('id', question_data.get('question'))
        relevant_chunks = question_chunk_mapping.get(question_id, [])
        task = asyncio.create_task(process_question(client, question_data, relevant_chunks,chunks,rate_limiter))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    write_response("data/response.txt",results,questions)
    logger.info(f"Total API calls made: {api_calls}")
    logger.info(f"Total cached answer retrivals : {len(questions)-api_calls}")
    logger.info("Finished processing.")

if __name__ == "__main__":

    asyncio.run(main())

