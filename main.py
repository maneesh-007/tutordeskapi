from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.admin import router
from routes.category import router as category_router
from routes.stclass import router as stclass_router
from routes.student import router as student_router
from routes.feestructure import router as fee_structure_router
from routes.fee import router as fee_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Tutor Desk!"}

app.include_router(router)
app.include_router(category_router)
app.include_router(stclass_router)
app.include_router(student_router)
app.include_router(fee_structure_router)
app.include_router(fee_router)
