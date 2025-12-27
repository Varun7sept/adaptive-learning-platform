# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# MONGO_DB = os.getenv("MONGO_DB", "adaptive_learning")

# client = MongoClient(MONGO_URI)
# db = client[MONGO_DB]

# # Collections
# quiz_evaluations = db["quiz_evaluations"]          # raw LLM results
# student_performance = db["student_performance"]    # normalized structured results
# spark_metrics = db["spark_metrics"]                # aggregated spark outputs
# exam_readiness = db["exam_readiness"]  
# practice_questions = db.practice_questions
# # Learning Path collection
# learning_path_collection = db["learning_paths"]

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "adaptive_learning")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Collections
quiz_evaluations = db["quiz_evaluations"]          # raw LLM results
student_performance = db["student_performance"]    # normalized structured results
spark_metrics = db["spark_metrics"]                # aggregated spark outputs

exam_readiness = db["exam_readiness"]
practice_questions = db["practice_questions"]

# ✅ NEW - Learning Path Collection
learning_path_collection = db["learning_paths"]
