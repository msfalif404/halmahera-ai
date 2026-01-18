import operator
from typing import Annotated, List, Literal, TypedDict, Union

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

# Function imports from existing controllers/services to wrap as tools
from controller.scholarship_controller import ScholarshipController
from controller.application_controller import ApplicationController
from core.models import ApplicationCreate, TaskCreate

# --- 1. Define Tools ---

@tool
def search_scholarships(query: str):
    """
    Search for scholarships based on the query. 
    Use this when the user is looking for new scholarships or asks about available opportunities.
    """
    return ScholarshipController.search_scholarship(query, k=5)

@tool
async def create_application(
    scholarship_id: str, 
    applicant_name: str, 
    email: str, 
    essay: str, 
    gpa: float
):
    """
    Create a new scholarship application.
    Use this ONLY when the user has explicitly confirmed they want to apply for a SPECIFIC scholarship.
    You must collect all necessary information (name, email, essay/motivation, GPA) before calling this.
    """
    # Construct the Pydantic model
    app_data = ApplicationCreate(
        scholarship_id=scholarship_id,
        applicant_name=applicant_name,
        email=email,
        essay=essay,
        gpa=gpa,
        status="Pending" 
    )
    return await ApplicationController.create_application(app_data)

@tool
async def create_tasks(application_id: str, tasks: List[dict]):
    """
    Create a preparation roadmap (list of tasks) for an application.
    Use this ONLY after an application has been successfully created AND the user has agreed to a preparation plan.
    'tasks' should be a list of dictionaries, each containing: 'title', 'description', 'priority' (High/Medium/Low), 'due_date' (YYYY-MM-DD).
    """
    results = []
    for task in tasks:
        # We dummy-fill due_date for now if missing or handle string conversion if needed
        # ideally the LLM provides valid ISO dates strings.
        task_data = TaskCreate(
            application_id=application_id,
            title=task.get("title"),
            description=task.get("description"),
            priority=task.get("priority", "Medium"),
            due_date=task.get("due_date") 
        )
        res = await ApplicationController.create_task(task_data)
        results.append(res)
    return {"status": "success", "created_tasks": results}


# --- 2. Define State ---

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 3. Define Nodes ---

# Initialize LLM
from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

# Bind tools
tools = [search_scholarships, create_application, create_tasks]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: AgentState):
    """
    The main chatbot node that decides whether to call a tool or respond to the user.
    """
    messages = state["messages"]
    
    # System Prompt injection
    system_prompt = SystemMessage(content="""
    You are the AI Scholarship Assistant. Your goal is to help students find scholarships, apply for them, and create preparation task lists.
    
    STRICT FLOW TO FOLLOW:
    1. **Search**: When user asks, search for scholarships. Present results clearly.
    2. **Selection**: User MUST explicitly select a scholarship before applying.
    3. **Application**: 
       - Gather: Name, Email, GPA, and a short Essay/Motivation.
       - Confirm details with user.
       - Call `create_application`.
    4. **Roadmap**: 
       - AFTER application is created, suggest a preparation plan.
       - If user agrees, generate specific tasks (e.g., "Study for IELTS", "Fix CV").
       - Call `create_tasks`.
    
    Be helpful, professional, and do not hallucinate scholarship details. Use the search tool.
    """)
    
    # Ensure system prompt is always at the start purely for context, 
    # but in LangGraph usually we just prepend if it's not there.
    # For simplicity, we just pass it in the invocation if we want, or prepend here.
    if not isinstance(messages[0], SystemMessage):
        messages = [system_prompt] + messages
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# --- 4. Build Graph ---

graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

def route_tools(state: AgentState):
    """
    Check if the last message has tool calls.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get("messages", [])):
        ai_message = messages[-1]
    elif isinstance(state, BaseMessage):
        ai_message = state
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END}
)

graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()
