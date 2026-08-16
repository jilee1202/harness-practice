"""사용 가능한 쿠폰 목록.

실제 서비스라면 DB에 있겠지만, 연습용이라 코드 안에 둔다.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Coupon:
    code: str
    kind: str  # "amount" = 정액 할인, "rate" = 정률 할인
    value: float  # amount면 원, rate면 비율(0.1 = 10%)
    label: str


COUPONS: Dict[str, Coupon] = {
    "WELCOME5000": Coupon("WELCOME5000", "amount", 5000, "신규 가입 5,000원 할인"),
    "SPRING10": Coupon("SPRING10", "rate", 0.10, "봄맞이 10% 할인"),
    "BIGSALE": Coupon("BIGSALE", "amount", 50000, "대형 할인 50,000원"),
}


def find_coupon(code: Optional[str]) -> Optional[Coupon]:
    """쿠폰 코드로 쿠폰을 찾는다. 없으면 None."""
    if not code:
        return None
    return COUPONS.get(code.strip().upper())
