# from kafka import KafkaProducer
# import json

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'],  # Kafka server
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')  # serialize JSON
# )

# def send_evaluation_event(student_id: str, quiz_id: str, score: float, total: int):
#     """
#     Sends a student's quiz evaluation result to Kafka topic.
#     """
#     message = {
#         "student_id": student_id,
#         "quiz_id": quiz_id,
#         "score": score,
#         "total": total,
#         "accuracy": round((score / total) * 100, 2)
#     }
#     try:
#         producer.send('quiz_evaluations', value=message)
#         producer.flush()
#         return {"status": "sent", "data": message}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

from kafka import KafkaProducer
import json

producer = None  # create later (lazy initialization)

def get_producer():
    global producer

    # Create producer ONLY when needed (not at import time)
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=5
            )
            print("✅ Kafka Producer connected successfully.")
        except Exception as e:
            print("❌ Kafka Producer connection failed:", e)
            producer = None

    return producer


def send_evaluation_event(student_id: str, quiz_id: str, score: float, total: int):
    """
    Safely sends a student's quiz evaluation result to Kafka.
    Backend will NOT crash even if Kafka is offline.
    """

    message = {
        "student_id": student_id,
        "quiz_id": quiz_id,
        "score": score,
        "total": total,
        "accuracy": round((score / total) * 100, 2)
    }

    try:
        p = get_producer()

        if p is None:
            return {"status": "error", "error": "Kafka not connected"}

        p.send("quiz_evaluations", value=message)
        p.flush()
        return {"status": "sent", "data": message}

    except Exception as e:
        return {"status": "error", "error": str(e)}
