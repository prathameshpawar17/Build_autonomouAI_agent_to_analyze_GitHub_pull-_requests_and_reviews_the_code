import requests
from celery import Celery
from ..db.postgres import update_task_status
from ..db.models import SessionLocal
from ..config import Config
from ..logger import logging
from ..core.github_utils import fetch_pr_files
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = Celery(
    "tasks",
    broker=Config.REDIS_URL,  # Redis for message queuing
    backend=Config.REDIS_URL  # PostgreSQL for task results
)

@app.task(bind=True)
def analyze_pr_task(self, repo_url: str, pr_number: int):
    session = SessionLocal()
    try:
        # Fetch PR files (use GitHub API)
        files = fetch_pr_files(repo_url, pr_number)
        if not files:
            raise Exception("No files found in the PR.")

        # Initialize LangChain OpenAI model
        llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4"
        )

        # Define prompt for analysis
        prompt = PromptTemplate(
            input_variables=["file_name", "content"],
            template="""
                Analyze the following GitHub Pull Request file for potential issues:
                File Name: {file_name}
                Content:
                {content}
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt)

        # Analyze each file in the PR
        results = []
        for file in files:
            analysis = chain.run(file_name=file["filename"], content=file["content"])
            results.append({
                "file_name": file["filename"],
                "analysis": analysis,
            })

        # Update task status in DB
        update_task_status(self.request.id, "completed", result=results, db=session)
        return results
    except Exception as e:
        update_task_status(self.request.id, "failed", result=str(e), db=session)
        logging.error(f"Task {self.request.id} failed: {e}")
        raise
    finally:
        session.close()


# import requests
# from celery import Celery
# from ..db.postgres import update_task_status
# from ..db.models import SessionLocal
# from ..config import settings
# from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
# from ..core.github_utils import fetch_pr_files
# from ..logger import logging

# #logging.error(f"Task {self.request.id} failed: {e}")

# app = Celery(
#     "tasks",
#     broker=CELERY_BROKER_URL,  # Redis for message queuing
#     backend=CELERY_RESULT_BACKEND  # PostgreSQL for task results
# )

# @app.task(bind=True)
# def analyze_pr_task(self, repo_url: str, pr_number: int):
#     session = SessionLocal()
#     try:
#         # Fetch PR files (use GitHub API)
#         files = fetch_pr_files(repo_url, pr_number)
#         if not files:
#             raise Exception("No files found in the PR.")

#         # Analyze files using Ollama API
#         results = []
#         for file in files:
#             response = requests.post(
#                 "https://api.ollama.com/analyze",
#                 headers={"Authorization": f"Bearer {settings.ollama_api_key}"},
#                 json={"content": file["content"]},
#             )
#             response.raise_for_status()
#             results.append({
#                 "file_name": file["name"],
#                 "analysis": response.json(),
#             })

#         # Update task status in DB
#         update_task_status(self.request.id, "completed", result=results, db=session)
#         return results
#     except Exception as e:
#         update_task_status(self.request.id, "failed", result=str(e), db=session)
#         raise
#     finally:
#         session.close()


# # import requests
# # from celery import Celery
# # from ..db.redis import get_redis_client
# # from ..core.github_utils import fetch_pr_files
# # from ..config import settings

# # app = Celery("tasks", broker=settings.redis_url, backend=settings.redis_url)

# # @app.task
# # def analyze_pr_task(repo_url: str, pr_number: int):
# #     try:
# #         # Step 1: Fetch PR files
# #         files = fetch_pr_files(repo_url, pr_number)
# #         if not files:
# #             raise Exception("No files found in the pull request.")

# #         # Step 2: Analyze files using Ollama API
# #         results = []
# #         for file in files:
# #             response = requests.post(
# #                 "https://api.ollama.com/analyze",
# #                 headers={"Authorization": f"Bearer {settings.ollama_api_key}"},
# #                 json={"content": file["content"]},
# #             )
# #             if response.status_code != 200:
# #                 raise Exception(f"Ollama API error: {response.text}")

# #             results.append({
# #                 "name": file["name"],
# #                 "analysis": response.json(),
# #             })

# #         # Step 3: Save results to Redis
# #         redis_client = get_redis_client()
# #         redis_client.set(f"task:{analyze_pr_task.request.id}:results", results)
# #         return results
# #     except Exception as e:
# #         raise Exception(f"Task failed: {str(e)}")
