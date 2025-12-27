# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware   # ✅ add this import
# from app.routes import quiz_routes, quiz_eval_routes  # ✅ import your routes file

# # Create FastAPI app
# app = FastAPI()

# # ✅ Enable CORS so React (running on localhost:5173) can call FastAPI
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 👈 for now allow all origins (you can restrict later)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Include your routes
# app.include_router(quiz_routes.router, prefix="/api")
# app.include_router(quiz_eval_routes.router, prefix="/api")

# @app.get("/")
# def root():
#     return {"message": "Backend is running successfully!"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules
from app.routes import quiz_routes
from app.routes import quiz_eval_routes
from app.routes import agent_routes   # ✅ Agentic AI routes

# Create FastAPI app
app = FastAPI(
    title="Adaptive Learning Platform Backend",
    description="Backend for Quiz Generation, Evaluation, Agentic AI, Kafka, and MongoDB",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later change to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(quiz_routes.router, prefix="/api")
app.include_router(quiz_eval_routes.router, prefix="/api")
app.include_router(agent_routes.router, prefix="/api")  # ✅ Agent routes available

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}




