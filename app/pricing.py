"""주문 요금 계산 규칙.

계산 순서는 docs/pricing-rules.md 에 한국어로 설명해 두었다.
순서가 바뀌면 최종 금액이 달라지므로 함부로 바꾸지 않는다.
"""

from .coupons import find_coupon
from .models import Grade, OrderRequest, PriceBreakdown

# 등급별 할인율
GRADE_DISCOUNT_RATE = {
    Grade.NORMAL: 0.00,
    Grade.SILVER: 0.03,
    Grade.GOLD: 0.05,
    Grade.VIP: 0.10,
}

# 배송비 정책
SHIPPING_FEE = 3000
FREE_SHIPPING_THRESHOLD = 50000


def calculate_price(order: OrderRequest) -> PriceBreakdown:
    """주문을 받아 각 단계 금액을 계산한다."""
    notes = []

    # ① 상품 합계
    subtotal = sum(item.unit_price * item.quantity for item in order.items)
    notes.append(f"상품 {len(order.items)}종 합계 {subtotal:,}원")

    # ② 등급 할인 — 상품 합계에서 뺀다
    rate = GRADE_DISCOUNT_RATE[order.grade]
    grade_discount = round(subtotal * rate)
    after_grade = subtotal - grade_discount
    if grade_discount:
        notes.append(f"{order.grade.value} 등급 {rate:.0%} 할인 -{grade_discount:,}원")
    else:
        notes.append(f"{order.grade.value} 등급은 할인 없음")

    # ③ 쿠폰 할인 — 등급 할인이 적용된 금액에서 다시 뺀다
    #    할인액이 남은 금액보다 크면 0원에서 멈춘다 (음수 방지)
    coupon = find_coupon(order.coupon_code)
    coupon_discount = 0
    if coupon is None:
        if order.coupon_code:
            notes.append(f"쿠폰 '{order.coupon_code}' 를 찾을 수 없어 무시함")
        else:
            notes.append("쿠폰 없음")
    elif coupon.kind == "amount":
        coupon_discount = int(coupon.value)
        notes.append(f"쿠폰 {coupon.label} -{coupon_discount:,}원")
    else:
        coupon_discount = round(after_grade * coupon.value)
        notes.append(f"쿠폰 {coupon.label} -{coupon_discount:,}원")

    after_coupon = max(0, after_grade - coupon_discount)
    if after_grade - coupon_discount < 0:
        notes.append("쿠폰 할인액이 상품 금액을 초과하여 0원으로 고정")

    # ④ 배송비 — 무료 기준은 '할인 전' 상품 합계로 판단한다
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        shipping_fee = 0
        notes.append(f"상품 합계가 {FREE_SHIPPING_THRESHOLD:,}원 이상이라 배송비 무료")
    else:
        shipping_fee = SHIPPING_FEE
        notes.append(f"배송비 {SHIPPING_FEE:,}원")

    # ⑤ 최종 금액
    total = after_coupon + shipping_fee

    return PriceBreakdown(
        subtotal=subtotal,
        grade_discount=grade_discount,
        after_grade=after_grade,
        coupon_code=coupon.code if coupon else None,
        coupon_discount=coupon_discount,
        after_coupon=after_coupon,
        shipping_fee=shipping_fee,
        total=total,
        notes=notes,
    )
