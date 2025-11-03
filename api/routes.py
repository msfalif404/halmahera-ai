from fastapi import APIRouter, Query

from controller.application_controller import ApplicationController
from controller.scholarship_controller import ScholarshipController
from core.models import ApplicationCreate, TaskCreate

router = APIRouter()

@router.get("/")
def get_all_scholarships(limit: int = 100):
    """
    Retrieve a list of all available scholarships.
    The model should present scholarship options clearly and concisely.
    Limit the result to 100 items per request to avoid information overload.
    """
    return ScholarshipController.get_all_scholarships(limit)

@router.get("/search")
def search_scholarship(query: str = Query(..., description="Search query text")):
    """
    Search for scholarships that best match the user's input query using semantic search.

    CRITICAL FLOW CONTROL:
    - ONLY return the most relevant scholarships that match the user's query precisely
    - DO NOT include scholarships from unrelated countries or fields
    - After presenting results, ask the user if they want to apply for any specific scholarship
    - DO NOT proceed to any other steps until user selects a scholarship

    The model must:
    - Filter results strictly based on query semantics (e.g., "Sweden" should only show Swedish scholarships)
    - Present results in clear bullet points with: name, deadline, eligibility, country
    - Wait for user to explicitly choose a scholarship before suggesting next steps
    - Only mention application process AFTER user selects a specific scholarship
    """
    return ScholarshipController.search_scholarship(query, k=10)

@router.post("/applications")
async def create_application(application_data: ApplicationCreate):
    """
    Create a new scholarship application record for the user's selected scholarship.

    STRICT FLOW SEQUENCE:
    1. Guide user through filling ALL required fields for the chosen scholarship
    2. Proactively ask for clarification if information is missing
    3. After successful creation, CONFIRM successful registration with key details:
       - Scholarship name
       - Application ID  
       - Deadline
       - Important requirements/reminders
    4. Ask user if they want to get a personalized preparation plan recommendation

    CRITICAL RULES:
    - DO NOT call create_task endpoint from here
    - DO NOT create tasks until AFTER user agrees to the recommended plan
    - ONLY ask about preparation plan recommendation after confirming application success
    - Wait for user's explicit agreement before showing plan recommendation

    This continues the flow: search_scholarship → [user selects] → create_application → [recommend plan] → create_task
    """
    return await ApplicationController.create_application(application_data)

@router.get("/applications")
async def list_applications():
    """
    Retrieve all scholarship applications submitted by the user.
    The model can summarize each application's current status, deadlines, and progress.
    """
    return await ApplicationController.list_applications()

@router.get("/applications/{application_id}")
async def get_application_by_id(application_id: str):
    """
    Retrieve detailed information for a specific scholarship application identified by its ID.
    The model can highlight key details such as deadlines, required documents, or next steps.
    """
    return await ApplicationController.get_application_by_id(application_id)

@router.post("/tasks")
async def create_task(task_data: TaskCreate):
    """
    Create a new task roadmap for the user's scholarship application process.

    STRICT FLOW REQUIREMENTS:
    - This endpoint should ONLY be called AFTER:
      1. User has successfully created an application AND
      2. LLM has confirmed the application was registered AND  
      3. LLM has asked if user wants a preparation plan recommendation AND
      4. User has explicitly agreed to see the recommendation AND
      5. LLM has presented a detailed preparation plan with multiple tasks AND
      6. User has explicitly agreed to create the tasks

    Steps:
    1. First, present a detailed preparation plan recommendation with 5-8 specific tasks
       (e.g., IELTS preparation, CV preparation, recommendation letters, etc.)
    2. Ask user if they want to create these tasks in the system
    3. If user agrees, create multiple specific tasks with realistic timelines
    4. Each task should have:
       - Clear description (e.g., "Prepare IELTS test with target score 7.0")
       - Specific start and end dates based on scholarship deadline
       - Priority level
    5. Summarize all created tasks and confirm with user

    The model must:
    - Create MULTIPLE specific tasks, not just one general task
    - Ensure tasks are realistic and time-bound
    - Get user confirmation before actually creating the tasks
    """
    return await ApplicationController.create_task(task_data)

@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: str):
    """
    Retrieve details and progress for a specific task in the user's scholarship roadmap.
    The model can provide suggestions or reminders to help the user complete their tasks on time.
    """
    return await ApplicationController.get_task_by_id(task_id)