"""요금 계산 규칙이 문서대로 동작하는지 확인한다."""

from app.models import Grade, OrderItem, OrderRequest
from app.pricing import calculate_price


def order(items, grade=Grade.NORMAL, coupon=None, weekend=False):
    return OrderRequest(
        items=[OrderItem(name=n, unit_price=p, quantity=q) for n, p, q in items],
        grade=grade,
        coupon_code=coupon,
        is_weekend=weekend,
    )


def test_할인_없는_주문은_상품합계에_배송비만_더한다():
    r = calculate_price(order([("텀블러", 12000, 1)]))
    assert r.subtotal == 12000
    assert r.grade_discount == 0
    assert r.shipping_fee == 3000
    assert r.total == 15000


def test_골드등급은_5퍼센트_할인된다():
    r = calculate_price(order([("텀블러", 12000, 3)], grade=Grade.GOLD))
    assert r.subtotal == 36000
    assert r.grade_discount == 1800
    assert r.after_grade == 34200


def test_문서에_적힌_예시와_금액이_같다():
    # 12,000원 3개 / 골드 / WELCOME5000 → 32,200원
    r = calculate_price(order([("텀블러", 12000, 3)], grade=Grade.GOLD, coupon="WELCOME5000"))
    assert r.subtotal == 36000
    assert r.grade_discount == 1800
    assert r.coupon_discount == 5000
    assert r.after_coupon == 29200
    assert r.shipping_fee == 3000
    assert r.total == 32200


def test_상품합계가_5만원_이상이면_배송비가_무료다():
    r = calculate_price(order([("의자", 50000, 1)]))
    assert r.shipping_fee == 0
    assert r.total == 50000


def test_정률쿠폰은_등급할인_후_금액에서_계산된다():
    r = calculate_price(order([("텀블러", 10000, 2)], grade=Grade.VIP, coupon="SPRING10"))
    assert r.subtotal == 20000
    assert r.grade_discount == 2000  # VIP 10%
    assert r.after_grade == 18000
    assert r.coupon_discount == 1800  # 18,000의 10%


def test_없는_쿠폰코드는_무시된다():
    r = calculate_price(order([("텀블러", 10000, 1)], coupon="NOPE"))
    assert r.coupon_discount == 0
    assert r.coupon_code is None
