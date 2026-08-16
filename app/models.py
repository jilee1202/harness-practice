"""주문 요금 계산 API에서 주고받는 데이터의 모양을 정의한다."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Grade(str, Enum):
    """회원 등급."""

    NORMAL = "일반"
    SILVER = "실버"
    GOLD = "골드"
    VIP = "VIP"


class OrderItem(BaseModel):
    """주문 항목 하나."""

    name: str = Field(..., description="상품명", examples=["텀블러"])
    unit_price: int = Field(..., ge=0, description="단가(원)", examples=[12000])
    quantity: int = Field(..., gt=0, description="수량", examples=[3])


class OrderRequest(BaseModel):
    """주문 요청."""

    items: List[OrderItem] = Field(..., min_length=1, description="주문 항목 목록")
    grade: Grade = Field(default=Grade.NORMAL, description="회원 등급")
    coupon_code: Optional[str] = Field(
        default=None, description="쿠폰 코드 (없으면 비워둔다)", examples=["WELCOME5000"]
    )
    is_weekend: bool = Field(
        default=False,
        description="주말 주문 여부. 현재 요금 계산에는 쓰이지 않는다.",
    )


class PriceBreakdown(BaseModel):
    """계산 결과. 각 단계 금액을 모두 보여준다."""

    subtotal: int = Field(..., description="① 상품 합계")
    grade_discount: int = Field(..., description="② 등급 할인액")
    after_grade: int = Field(..., description="등급 할인 후 금액")
    coupon_code: Optional[str] = Field(None, description="적용된 쿠폰 코드")
    coupon_discount: int = Field(..., description="③ 쿠폰 할인액")
    after_coupon: int = Field(..., description="쿠폰 할인 후 금액")
    shipping_fee: int = Field(..., description="④ 배송비")
    total: int = Field(..., description="⑤ 최종 결제 금액")
    notes: List[str] = Field(default_factory=list, description="계산 과정 설명")
