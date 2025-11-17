from kafka import KafkaProducer
import json

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # serialize JSON
)

def send_evaluation_event(student_id: str, quiz_id: str, score: float, total: int):
    """
    Sends a student's quiz evaluation result to Kafka topic.
    """
    message = {
        "student_id": student_id,
        "quiz_id": quiz_id,
        "score": score,
        "total": total,
        "accuracy": round((score / total) * 100, 2)
    }
    try:
        producer.send('quiz_evaluations', value=message)
        producer.flush()
        return {"status": "sent", "data": message}
    except Exception as e:
        return {"status": "error", "error": str(e)}
