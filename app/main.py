"""주문 요금 계산 API.

실행:  uvicorn app.main:app --reload
확인:  브라우저에서 http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .coupons import COUPONS
from .models import OrderRequest, PriceBreakdown
from .pricing import calculate_price

app = FastAPI(
    title="주문 요금 계산 API",
    description="주문 내용을 넣으면 각 단계 할인과 최종 결제 금액을 돌려준다.",
    version="0.1.0",
)


@app.get("/", include_in_schema=False)
def root():
    """루트로 들어오면 문서 화면으로 보낸다."""
    return RedirectResponse(url="/docs")


@app.get("/health", summary="서버가 살아 있는지 확인")
def health():
    return {"status": "ok"}


@app.get("/coupons", summary="사용 가능한 쿠폰 목록")
def list_coupons():
    return [
        {"code": c.code, "kind": c.kind, "value": c.value, "label": c.label}
        for c in COUPONS.values()
    ]


@app.post("/price", response_model=PriceBreakdown, summary="주문 요금 계산")
def price(order: OrderRequest) -> PriceBreakdown:
    return calculate_price(order)
