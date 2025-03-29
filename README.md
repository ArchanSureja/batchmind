# BatchMind 

**Batch prediction with Gemini APIs, leveraging long context and context caching for efficiently answering questions about a single video**

### Setup steps for local machine(Linux only): 

1. Clone Repository : `git clone https://github.com/ArchanSureja/batchmind.git`
2. Create virtual Environment : `python3 -m venv .venv`
3. Activate Virtual Environment : `source .venv/bin/activate`
4. Install Dependencies : `pip install -r requirements.txt`
5. Create .env file add These Variables : ``` MAX_CONCURRENT_REQUESTS=3
   LOG_LEVEL=INFO ```
7. Get API_KEY from Google AI Studio : [Google AI Studio](https://aistudio.google.com/)
8. Set the API_KEY in .env file : ` API_KEY=YOUR_API_KEY `

**Ensure redis server is running on your machine**
- If not installed then install redis server : `sudo apt install redis`
- redis server start command : `redis-server`
- connection checking : `redis-cli ping` it will return PONG if redis server is running 

### Usage :
stay in batchmind directory 

- **Get Transcript Using Youtube URL :** 
    - Command : `python3 src/get_transcript.py VIDEO_URL`


- **Add Questions with questions.json in data directory** 
    - Sample Questions.json file : 
  ```
  [
  {
      "id": "q1",
      "question": "What is the main topic discussed in the transcript?"
  },
  {
      "id": "q2",
      "question": "Can you summarize the key points covered?"
  },
  {
      "id": "q3",
      "question": "Who are the main speakers in the discussion?"
  },
  {
      "id": "q4",
      "question": "What problem or issue is being addressed?"
  },
  {
      "id": "q5",
      "question": "What solution or insights were provided regarding the issue?"
  },
  ] 
**Structure of json file must follow the Given Sample** 


- **Run the main.py script :**
    - command : `python3 src/main.py`
      
Resonpsoe will be stored in response.txt in data directory
      
You can view logs in logs directory 

- **Comparing serial and async Execution :**
    - Run Following Command : `python3 src/benchmark.py` 

Result will be avaible in Benchmarks directory

### Sample screenshots : 

#### main script : ![image](https://github.com/user-attachments/assets/e84fc483-160a-4cb8-8a5f-f65b1f5af402)

#### comparison between serial and async execution : ![image](https://github.com/user-attachments/assets/250bbba7-347f-4d0e-8b3f-35a94a1e40c4)
 




