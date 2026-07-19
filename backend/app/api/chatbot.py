from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.assistant.assistant import FalconAssistant


router = APIRouter(
    prefix="/chatbot",
    tags=["FalconAI Assistant"]
)


# =====================================================
# Assistant Instance
# =====================================================

assistant = FalconAssistant()


# =====================================================
# Request Models
# =====================================================

class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description="User message"
    )

    user_id: Optional[str] = None

    language: str = "ar"

    context: Optional[Dict[str, Any]] = None



class ChatResponse(BaseModel):

    success: bool

    response: str

    data: Optional[Dict[str, Any]] = None



# =====================================================
# Health Check
# =====================================================

@router.get("/health")
async def chatbot_health():

    return {

        "status": "online",

        "service": "FalconAI Assistant",

        "version": "1.0"

    }



# =====================================================
# Main Chat Endpoint
# =====================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat_with_assistant(
    request: ChatRequest
):

    try:


        result = assistant.chat(

            message=request.message,

            user_id=request.user_id,

            language=request.language,

            context=request.context

        )


        if isinstance(result, str):

            return {

                "success": True,

                "response": result,

                "data": None

            }



        return {

            "success": True,

            "response": result.get(
                "response",
                ""
            ),

            "data": result

        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail={

                "error": "Assistant processing failed",

                "message": str(e)

            }

        )



# =====================================================
# Trading Explanation Endpoint
# =====================================================

class ExplainRequest(BaseModel):

    signal: Dict[str, Any]

    language: str = "ar"



@router.post("/explain")
async def explain_signal(
    request: ExplainRequest
):

    try:


        explanation = assistant.explain_signal(

            request.signal,

            language=request.language

        )


        return {

            "success": True,

            "explanation": explanation

        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



# =====================================================
# Market Question Endpoint
# =====================================================

@router.post("/market-question")
async def market_question(
    request: ChatRequest
):

    try:


        answer = assistant.market_analysis(

            request.message,

            context=request.context

        )


        return {

            "success": True,

            "answer": answer

        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

)
