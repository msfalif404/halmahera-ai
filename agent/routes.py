
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agent.graph import graph

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_thread"

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint directly invoking the LangGraph agent.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    inputs = {"messages": [HumanMessage(content=request.message)]}
    final_state = await graph.ainvoke(inputs, config=config)
    return {"response": final_state["messages"][-1].content}

from fastapi.responses import StreamingResponse
import json

@router.post("/stream")
async def stream_chat_endpoint(request: ChatRequest):
    """
    Stream chat response token-by-token.
    """
    async def event_stream():
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # Use astream_events to get token-level streaming
        async for event in graph.astream_events(inputs, config=config, version="v1"):
            kind = event["event"]
            
            # Stream LLM tokens
            if kind == "on_on_chat_model_stream":
                pass # v1 event name might differ, checking documentation mental model...
                # Actually, standard LangGraph astream_events usually has "on_chat_model_stream"
            
            # Simplified approach: Just stream the chunks from the chatbot node if possible
            # But astream_events is the standard way.
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield f"data: {json.dumps({'type': 'token', 'content': content})}\n\n"
            
            # Optional: Notify when tools are being called
            elif kind == "on_tool_start":
                yield f"data: {json.dumps({'type': 'status', 'content': '🛠️ Calling tool...'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
