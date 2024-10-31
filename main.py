from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from cv_stripper import CVStripper
from bson.objectid import ObjectId
from database import Database

# Models
from classes.user import RegisterUser
from classes.user import LoginUser

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:420",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

database = Database()

cvStripper = CVStripper()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/pdf/{name}")
def pdf(name: str):
    path = f"uploads/resumes/{name}"
    
    extractedData = cvStripper.extract(path)
    return JSONResponse(extractedData)


@app.post("/pdf/")
async def pdf(file: UploadFile = File(...)):
    path = f"uploads/resumes/{file.filename}"

    # Save pdf
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
        
    extractedData = cvStripper.extract(path)
    return JSONResponse(extractedData)


@app.post("/savepdf/")
async def savepdf(file: UploadFile = File(...)):
    path = f"uploads/resumes/{file.filename}"

    # Save pdf
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
        
    extractedData = cvStripper.extract(path)
    
    result = database.getCollection("test-collection").insert_one(extractedData)
            
    return JSONResponse({ "success": True, "id": str(result.inserted_id) })


@app.get("/getpdf/{id}")
async def getpdf(id: str):
    document = database.getCollection("test-collection").find_one({ "_id": ObjectId(id) })
        
    document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
    
    return JSONResponse(document)


@app.get("/jobs/")
async def jobs():
    documents = list( database.getCollection("jobs").find())

    for document in documents:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(documents)


@app.get("/jobs/{id}")
async def jobs(id: str):
    document = database.getCollection("jobs").find_one({ "_id": ObjectId(id) })
    
    document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(document)


@app.get("/candidates/")
async def candidates():
    documents = list( database.getCollection("candidates").find())

    for document in documents:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(documents)





# new

@app.post("/candidates/create")
async def candidate(file: UploadFile = File(...)):
    path = f"uploads/resumes/{file.filename}"

    # Save pdf
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
        
    candidate = cvStripper.extract(path)
    
    result = database.getCollection("candidates").insert_one(candidate)
             
    return JSONResponse({ "success": True, "id": str(result.inserted_id) })


@app.post("/register")
async def register(userData: RegisterUser):
    if (userData.password != userData.password_check):
        return JSONResponse({ "success": False, "error": "passwords must match" })
    
    user = {
        "username": userData.username,
        "password": userData.password,
    }
        
    result = database.getCollection("users").insert_one(user)
            
    return JSONResponse({ "success": True, "id": str(result.inserted_id) })


@app.post("/login")
async def register(userData: LoginUser):
    foundUser = database.getCollection("users").find_one({ "username": userData.username })
    
    if (foundUser is not None and foundUser["password"] == userData.password):
        return JSONResponse({ "success": True, "_id": str(foundUser["_id"]) })
    
    return JSONResponse({ "success": False, "error": "Invalid login" })


@app.get("/users/{id}")
async def users(id: str):
    document = database.getCollection("users").find_one({ "_id": ObjectId(id) })
    
    document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(document)


@app.post("/users/{id}/cv")
async def cv(id: str, file: UploadFile = File(...)):
    path = f"uploads/resumes/{id}.pdf"            

    # Save pdf
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
        
    cvUser = cvStripper.extract(path)
    
    result = database.getCollection("users").update_one(
        {"_id": ObjectId(id)}, 
        {"$set": cvUser}
    )
    
    return JSONResponse({ "success": True })