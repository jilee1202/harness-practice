# harness-practice — 주문 요금 계산 API

AgentCore Harness 연습용 저장소. AI 에이전트에게 "요구사항을 주면 소스를 고쳐라"를
시켜보고, 그 결과를 **코드를 읽지 않고 동작으로 확인**하기 위한 작은 앱이다.

- 업무 규칙: [`docs/pricing-rules.md`](docs/pricing-rules.md) — 코드를 몰라도 읽을 수 있게 써 두었다
- 외부 의존 없음 — DB도, 외부 API도 필요 없다

---

## 실행 방법 (Windows PowerShell)

처음 한 번만:

```powershell
cd D:\_ai_source\harness-practice
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

이후 실행할 때마다:

```powershell
cd D:\_ai_source\harness-practice
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

브라우저에서 **http://127.0.0.1:8000/docs** 를 연다.

---

## 브라우저에서 확인하는 법

1. `/docs` 화면에서 **POST /price** 를 클릭
2. **Try it out** 버튼을 누른다
3. 아래 내용을 입력창에 붙여넣고 **Execute**

```json
{
  "items": [{ "name": "텀블러", "unit_price": 12000, "quantity": 3 }],
  "grade": "골드",
  "coupon_code": "WELCOME5000",
  "is_weekend": false
}
```

4. 아래 Response 칸에 각 단계 금액이 나온다. 최종 금액은 **32,200원**이어야 한다.

`notes` 항목에 "어디서 얼마가 깎였는지"가 한국어로 적혀 나온다.

---

## 테스트

```powershell
.\.venv\Scripts\Activate.ps1
pytest -v
```

모두 통과하면 규칙대로 동작하고 있다는 뜻이다.
소스를 고친 뒤에도 이 명령을 돌려 **통과 개수가 줄지 않았는지** 확인한다.

---

## 구성

```
app/
  models.py     주고받는 데이터의 모양
  coupons.py    쿠폰 목록
  pricing.py    계산 규칙 (핵심)
  main.py       API 입구
tests/
  test_pricing.py
docs/
  pricing-rules.md   업무 규칙서
```

---

## 연습용으로 시켜볼 만한 요구사항

`docs/pricing-rules.md` 마지막 절에 **일부러 애매하게 남겨둔 지점 세 개**가 있다.
에이전트에게 이런 걸 시켜보고 결과를 브라우저에서 확인한다.

- "쿠폰 할인이 상품 금액보다 크면 최종 금액을 0원으로 막아줘"
- "주말 주문은 배송비를 면제해줘"
- "배송비 무료 기준을 할인 후 금액으로 바꿔줘"
