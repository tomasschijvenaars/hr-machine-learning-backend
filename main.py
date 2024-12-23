from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from cv_stripper import CVStripper
from bson.objectid import ObjectId
from database import Database
from knn import KNN
from stringcompare import StringCompare

# Models
from classes.user import RegisterUser
from classes.user import LoginUser
from classes.job import Job
from classes.users import User
from classes.insert import AddData
from classes.users_score import Score
from classes.select_user import SelectUser

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

knn_script = KNN()
stringcompare = StringCompare()

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


@app.get("/jobs")
async def jobs():
    documents = list( database.getCollection("jobs").find())

    for document in documents:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(documents)


@app.get("/jobs/{id}")
async def jobs(id: str):
    document = database.getCollection("users").find_one({ "_id": ObjectId(id) })
    
    document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(document)


@app.post("/jobs")
async def jobs(job: Job):
    jobDict = vars(job)
    
    result = database.getCollection("jobs").insert_one(jobDict)
            
    return JSONResponse({ "success": True, "id": str(result.inserted_id) })


@app.get("/jobs/{id}/{userId}")
async def jobs(id: str, userId: str):    
    job = database.getCollection("jobs").find_one({ "_id": ObjectId(id) })
    user = database.getCollection("users").find_one({ "_id": ObjectId(userId) })

    user_skills = user["skills"]
    
    combined_skills = user_skills["programming_languages"] + user_skills["frameworks_and_tools"] + user_skills["soft_skills"]

    job_skills = job["skills"]

    skills_similarity = stringcompare.calculate_match_percentage(job_skills, combined_skills)

    job_experience_similarity = int(user["work_experience_total_years"]) / job["years_of_experience"] * 100

    sollicitant_perc = [skills_similarity, job_experience_similarity]

    users_with_job = list(database.getCollection("users").find({ "has_job": True }))

    array_users_with_job = [
    [obj["percent_skills"], obj["percent_experience"], int(obj["job_succesful"])]
    for obj in users_with_job
]   
    
    result = knn_script.classify_point(array_users_with_job, sollicitant_perc)

    #print(array_users_with_job)
    #print(sollicitant_perc)
    #print(result)

    return JSONResponse({ "result": result })

@app.get("/users")
async def users():
    documents = list( database.getCollection("users").find())

    for document in documents:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string for JSON serialization
            
    return JSONResponse(documents)

@app.post("/users")
async def users(user: User):
        user_dict = vars(user)

        result = database.getCollection("users").insert_one(user_dict)

        return JSONResponse({"success": True, "id": str(result.inserted_id)})

@app.get("/knn/{id}")
async def knn(id: str):    
    job = database.getCollection("jobs").find_one({ "_id": ObjectId(id) })
    jobless_users = list(database.getCollection("users").find({
        "$or": [
            { "has_job": False },
            { "has_job": { "$exists": False } }
        ]
    }))

    results = []

    for user in jobless_users:
        user_skills = user["skills"]
        
        combined_skills = user_skills["programming_languages"] + user_skills["frameworks_and_tools"] + user_skills["soft_skills"]

        job_skills = job["skills"]

        skills_similarity = stringcompare.calculate_match_percentage(job_skills, combined_skills)

        job_experience_similarity = int(user["work_experience_total_years"]) / job["years_of_experience"] * 100
        job_exp_check = min(job_experience_similarity, 100)

        sollicitant_perc = [skills_similarity, job_exp_check]
        users_with_job = list(database.getCollection("users").find({ "has_job": True }))

        array_users_with_job = [
            [obj["percent_skills"], obj["percent_experience"], int(obj["job_succesful"])]
            for obj in users_with_job
        ]
        
        result = knn_script.classify_point(array_users_with_job, sollicitant_perc)
        new_object = {
        "user": {
            "id":str(user["_id"]),  # Example value for 'result'
            "name": user["name"],  # Example value for 'result'
        },
        "skills_perc": skills_similarity,
        "experience_perc": job_exp_check,
        "result": result,  # Example value for 'result'
        # "sollicitant data": sollicitant_perc  # Example value for 'experience_percent'
    }

        print(result)

        results.append(new_object)

    return JSONResponse({ "results": results })


@app.post("/jobs/{jobId}/select-user/{userId}")
async def jobs(jobId: str, userId: str, insertdata: AddData):
    print(userId)

    print(insertdata)

    temp1 = vars(insertdata)

    result = database.getCollection("users").update_one(
        {"_id": ObjectId(userId)},
        {"$set": {
            "percent_skills": temp1["percent_skills"],
            "percent_experience": temp1["percent_experience"],
            "job_succesful": temp1["job_succesful"],
            "has_job": True
        }}
    )

    result = database.getCollection("jobs").update_one(
         {"_id": ObjectId(jobId)},
         {"$set": {"disabled": True}}
    )

            
    # return JSONResponse({ "success": True, "id": str(result) })
    return JSONResponse({ "success": True })