from fastapi import APIRouter

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get("/")
async def get_payments():
    return {
        "success": True,
        "message": "Payments list"
    }


@router.get("/methods")
async def payment_methods():
    return {
        "success": True,
        "methods": [
            "Visa",
            "MasterCard",
            "American Express",
            "PayPal",
            "Stripe",
            "Apple Pay",
            "Google Pay",
            "Binance Pay",
            "USDT",
            "USDC",
            "Bitcoin",
            "Ethereum",
            "Bank Transfer"
        ]
    }


@router.post("/create")
async def create_payment():
    return {
        "success": True,
        "message": "Payment created"
    }


@router.post("/verify")
async def verify_payment():
    return {
        "success": True,
        "message": "Payment verified"
    }


@router.post("/refund")
async def refund_payment():
    return {
        "success": True,
        "message": "Refund completed"
    }


@router.get("/{payment_id}")
async def payment_details(payment_id: int):
    return {
        "success": True,
        "payment_id": payment_id
    }
