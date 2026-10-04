# Plan: การจองงานบริการซ่อมบำรุง (UC-07)

อ้างอิง: spec.md SPEC-BOOKING v1.3 Draft v2 | Updated: 2569-10-04 | ร่างด้วย /plan

## 1. สรุปแนวทาง

- ลูกค้าที่ลงทะเบียนค้นช่างและช่วงเวลาตามประเภทงาน ที่อยู่ และช่วง 7 วันถัดไป แล้วล็อก slot 10 นาที (REQ-FN-008, REQ-FN-041, AS-06)
- ระบบตรวจการจองซ้อนและระยะบริการไม่เกิน 15 กิโลเมตรผ่าน BR-02, BR-03 และ IF-03
- ระบบสร้างงานและชำระด้วย authorize แล้ว capture; หาก gateway ไม่ตอบให้ status-inquiry ด้วย reference เดิมตาม ASM-08, ASM-09
- ระบบเข้าคิวแจ้งลูกค้าและช่างหลังสร้างงานตาม REQ-FN-012 และ ASM-10
- ระบบแยกสิทธิ์มุมมองช่าง ไม่ลงเบอร์ใน log และคงประวัติสถานะ 24 เดือนก่อนลบตาม REQ-SEC-004, REQ-PRV-002, REQ-DAT-002

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Payment Gateway รายเดิม (IF-01) | REQ-CON-003 | ใช้ interface `Gateway`; test ใช้ `FakeGateway` ที่จำลอง approved, declined และ timeout ตาม ASM-09 |
| Python 3.12 + FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ค่าเริ่มต้นของรายวิชา |
| SQLAlchemy 2 + PostgreSQL 16 | ทีมเลือกเอง ไม่ได้มาจาก spec | ต่อฐานข้อมูลผ่าน `DATABASE_URL`; test ใช้ `sqlite:///:memory:` |
| pytest + httpx (TestClient) | ทีมเลือกเอง ไม่ได้มาจาก spec | ทุก test ชื่อขึ้นต้น test_AC_07_xx |
| React 19 (Vite) + Tailwind CSS 4 | ทีมเลือกเอง ไม่ได้มาจาก spec | โครงเริ่มต้นอยู่ใน `frontend/` แล้ว |
| Vitest + React Testing Library | ทีมเลือกเอง ไม่ได้มาจาก spec | test หน้าจอใช้ API จำลอง ไม่ต้องรันหลังบ้าน |
| คิวในหน่วยความจำ (notify/queue.py) | ทีมเลือกเอง ไม่ได้มาจาก spec | วางข้อความและ retry ตาม ASM-10; test อ่านคิวโดยตรง |

library ทั้งหมดอยู่ใน `backend/requirements.txt`
รัน test หลังบ้าน: `cd backend && pytest -v -k "AC_"`
เปิดหลังบ้าน: `cd backend && uvicorn app.main:app --reload --port 8000` (หน้าจอเรียกผ่าน `/api` ซึ่ง Vite ส่งต่อให้)
รัน test หน้าจอ: `cd frontend && npm test` เปิดดูหน้าจอ: `cd frontend && npm run dev`

### โครงไฟล์

```
backend/
  requirements.txt
  pytest.ini
  app/
    main.py                     สร้าง FastAPI app รวม router และสร้างตารางตอนเริ่ม
    config.py                   DATABASE_URL, HOLD_MINUTES (ASM-08), GATEWAY_TIMEOUT_SECONDS (ASM-09), PHONE_REVEAL_HOURS (ASM-13)
    db/models.py                ตาราง customers, service_addresses, technicians, time_slots, jobs, job_status_history, payments, refunds
    db/session.py               engine, SessionLocal, get_db
    db/migrations/m001_init.py  ฟังก์ชัน upgrade(engine) สร้างทุกตาราง
    clock.py                    เวลาปัจจุบันที่ test กำหนดได้ (now=...)
    technicians/service.py      ค้นช่างว่าง (REQ-FN-008, BR-02, BR-03, IF-03, AS-06) และหาช่วงใกล้เคียง (AC-07-04)
    technicians/router.py       GET /technicians
    payments/service.py         authorize + timeout + status-inquiry + capture (REQ-IF-001, REQ-IF-005, ASM-08, ASM-09)
    booking/service.py          ล็อกช่วงเวลา (REQ-FN-041) และสร้างงาน (REQ-FN-008)
    refund/service.py           ยกเลิกงานและสร้าง Refund (REQ-BR-001, ASM-11)
    booking/router.py           POST /slots/{id}/hold, POST /bookings, GET /jobs/{id}, GET /jobs/{id}/technician-view
    notify/queue.py             คิวข้อความและ retry (REQ-FN-012, ASM-10)
    payments/gateway.py         interface Gateway + FakeGateway (IF-01)
    payments/service.py         authorize + timeout + status-inquiry + capture (REQ-IF-001, REQ-IF-005, ASM-08, ASM-09)
    logging                     ไม่มีตาราง log; privacy.py กรองรูปแบบเบอร์โทรออก (REQ-PRV-002)
    refund/service.py           ยกเลิกงานและสร้าง Refund (REQ-BR-001)
    refund/router.py            POST /jobs/{id}/cancel
    notify/queue.py             คิวข้อความและเวลาส่ง (REQ-FN-012)
    privacy.py                  ตัวกรอง log ไม่ให้มีเบอร์โทร (REQ-PRV-002)
  tests/
    conftest.py                 ฐานข้อมูลในหน่วยความจำ, FakeGateway, นาฬิกาจำลอง, ข้อมูลตั้งต้น (ช่าง ประสิทธิ์ ฯลฯ)
    test_booking.py             AC-07-01, 02, 03, 04
    test_payment.py             AC-07-05, 06, 07
    test_privacy.py             AC-07-09
    test_refund.py              AC-07-10 (R1 ถึง R6; R3 ตอบ 409 ตาม ASM-11)
    test_load_scaled.py         AC-07-08 แบบย่อส่วนตาม ASM-12
frontend/
  src/api/client.js             เรียก API ตามสัญญาข้อ 4
  src/pages/TechnicianPicker.jsx   เลือกประเภทงาน ที่อยู่ แล้วเลือกช่างและช่วงเวลา (ล็อก)
  src/pages/ConfirmBooking.jsx     แสดงราคา มัดจำ เงื่อนไข BR-01 แล้วกดยืนยัน รับ 409 แสดงช่วงใกล้เคียง
  src/pages/BookingResult.jsx      แสดงหมายเลขงานและสถานะ
  src/__tests__/AC-07-04.test.jsx  test หน้าจอของ AC-07-04
```

## 3. โมเดลข้อมูล

| ตาราง | ฟิลด์หลัก | รองรับ |
|---|---|---|
| customers | id, name, phone (PII) | REQ-PRV-002 |
| service_addresses | id, customer_id, text, geoPoint (lat, lng) ภายในระบบ | AS-03, BR-03, ASM-14 |
| technicians | id, name, skills (คั่นด้วยจุลภาค), base_lat, base_lng | BR-03 |
| time_slots | id, technician_id, start, end, state (ว่าง / ล็อกชั่วคราว / จองแล้ว), held_by_customer_id, hold_expires_at | REQ-FN-041, BR-02, AS-07 |
| jobs | id, customer_id, technician_id, slot_id, address_id, category, status (8 ค่า), deposit_amount, scheduled_start, created_at | REQ-FN-008, REQ-DAT-002 |
| job_status_history | id, job_id, from_status, to_status, at | REQ-DAT-002 (ประวัติ 24 เดือน) |
| payments | id, job_id, amount, gateway_ref, result (สำเร็จ / ล้มเหลว / หมดเวลา), authorized_at, captured_at | REQ-IF-001, REQ-IF-005, ASM-08, ASM-09 |
| refunds | id, job_id, amount, rule (R1..R6) | REQ-BR-001 |

- ตาราง log ไม่มี ระบบใช้ logging ผ่าน privacy.py ที่กรองรูปแบบเบอร์โทรออก (REQ-PRV-002)
- status ของ jobs ใช้ชื่อในโค้ดจาก glossary.md เท่านั้น (pending_payment, confirmed, auto_cancelled, rematching, en_route, in_progress, done, cancelled)

## 4. API / หน้าจอ

| รายการ | input / output หลัก | รองรับ |
|---|---|---|
| GET /technicians | in: category, address_id, customer_id / out: ช่างและช่วงเวลาที่ว่างใน 7 วันถัดไป ไม่เกิน 15 กิโลเมตร | REQ-FN-008, BR-02, BR-03, IF-03, AS-06 |
| POST /slots/{slot_id}/hold | in: customer_id / out: hold_expires_at หรือ 409 ถ้าถูกล็อกโดยคนอื่น | REQ-FN-041 |
| POST /bookings | in: customer_id, slot_id, address_id, category / out: 201 job confirmed, 409 slot_taken พร้อม alternatives หรือ 402 payment_failed | REQ-FN-008, REQ-IF-001, REQ-IF-005, AC-07-01, AC-07-04, ASM-08, ASM-09 |
| GET /jobs/{id} | out: งานและสถานะ (มุมมองลูกค้า) | REQ-FN-008 |
| GET /jobs/{id}/technician-view | in: technician_id / out: งาน; customer_phone เฉพาะ 2 ชั่วโมงก่อนนัดจนปิดงานตาม ASM-13 | REQ-SEC-004, ASM-13 |
| POST /jobs/{id}/cancel | in: cancelled_by / out: สถานะใหม่และ refund ตาม R1-R6 หรือ 409 สำหรับ R3 และ R6 | REQ-BR-001, ASM-11 |
| GET /notifications/queue | out: ข้อความที่เข้าคิวและสถานะ retry สำหรับลูกค้าและช่าง | REQ-FN-012, IF-02, ASM-10 |
| หน้าเลือกช่าง (TechnicianPicker) | เรียก GET /technicians แล้ว POST /slots/{id}/hold | REQ-FN-008, REQ-FN-041 |
| หน้ายืนยัน (ConfirmBooking) | แสดงมัดจำและ BR-01 แล้ว POST /bookings ถ้าได้ 409 แสดง "ช่วงเวลาถูกจองแล้ว" และปุ่มเลือกช่วงใกล้เคียง | AC-07-04 |
| หน้าผลการจอง (BookingResult) | แสดงหมายเลขงานและสถานะ "ยืนยันแล้ว" | REQ-FN-008 |

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| REQ-CON-003 | ข้อ 2 และ payments/gateway.py: ใช้ gateway รายเดิมผ่าน interface | ใช้แล้ว |
| REQ-CON-001 | ข้อ 7: ไม่ทำ A2 ใน R1 (D-07-02) เพื่อคุมขอบเขต 8 สัปดาห์ | ใช้แล้ว |
| IF-01 | ข้อ 2, 3 และ 4: authorize, capture, refund และ status-inquiry ผ่าน Gateway | ใช้แล้ว |
| IF-02 | ข้อ 4: คิวแจ้งลูกค้าและช่างหลังสร้างงาน | ใช้แล้ว |
| IF-03 | ข้อ 3 และ GET /technicians: คำนวณระยะจาก geoPoint ไม่เกิน 15 กิโลเมตร | ใช้แล้ว |
| MD-CTX-01 | ข้อ 4: endpoint เชื่อมลูกค้า ช่าง gateway ระบบส่งข้อความ และแผนที่ | ใช้แล้ว |
| MD-DOM-01 | ข้อ 3: entities และความสัมพันธ์ Customer, Job, Slot, Payment, Refund | ใช้แล้ว |
| MD-STM-01 | ข้อ 3 และ 7: สถานะงาน 8 ค่าและ transition | ใช้แล้ว |
| MD-SEQ-07-05 | ข้อ 4 และ 7: ลำดับ authorize, status-inquiry, capture | ใช้แล้ว |
| REQ-PRV-002 | ข้อ 3 และ privacy.py: ไม่เก็บเบอร์ใน log | ใช้แล้ว |
| REQ-SEC-004 | ข้อ 4: technician-view เปิดเบอร์ตาม ASM-13 | ใช้แล้ว |
| REQ-DAT-002 | ข้อ 3 และ 7: status 8 ค่า, history 24 เดือน แล้วลบเกินกำหนด | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-07-01 | test_AC_07_01_booking_success | ล็อก slot, POST /bookings กับ FakeGateway approved แล้วตรวจ job confirmed, slot จองแล้ว, payment 1 รายการ |
| AC-07-02 | test_AC_07_02_slot_not_rebookable | ทำให้ slot จองแล้ว แล้ว GET /technicians ด้วยลูกค้าอื่น ตรวจว่าไม่มี slot นั้น |
| AC-07-03 | test_AC_07_03_notify_both_within_60s | หลังจองสำเร็จ อ่านคิว ตรวจว่ามีข้อความถึงลูกค้าและช่าง และ due_at ไม่เกิน created_at + 60 วินาที |
| AC-07-04 | test_AC_07_04_no_charge_when_slot_taken | ลูกค้าอื่นจองก่อน แล้วสมชายยืนยัน ตรวจ 409, ไม่มี payment ของสมชาย, alternatives อย่างน้อย 2 และห่างไม่เกิน 3 ชั่วโมง |
| AC-07-05 | test_AC_07_05_payment_timeout | FakeGateway ไม่ตอบ 30 วินาที แล้ว inquiry ด้วย ref เดิมตอบ unknown ตรวจ job auto_cancelled, slot ว่าง, ไม่มี payment สำเร็จ |
| AC-07-06 | test_AC_07_06_payment_declined | FakeGateway declined ตรวจ 402, job auto_cancelled, slot ว่าง, มีข้อความแจ้งลูกค้า |
| AC-07-07 | test_AC_07_07_inquiry_approved_no_double_charge | FakeGateway ไม่ตอบ แต่ inquiry ตอบ approved ตรวจ job confirmed, authorize ถูกเรียก 1 ครั้ง, payment สำเร็จ 1 รายการ |
| AC-07-08 | test_AC_07_08_search_under_load_scaled | ยิง GET /technicians แบบย่อส่วน 20 คำขอพร้อมกัน วัดจากค้นหาถึงยืนยันโดยไม่รวม gateway และรายงานว่าไม่ใช่การทดสอบ 500 คนจริงตาม ASM-12 |
| AC-07-09 | test_AC_07_09_phone_hidden_until_2h | technician-view ก่อน 2 ชั่วโมงไม่มี customer_phone, ตั้งแต่ 2 ชั่วโมงก่อนนัดจนปิดงานมี และตรวจ log ไม่มีเบอร์ตาม ASM-13 |
| AC-07-10 | test_AC_07_10_refund_R1_to_R6 | ตั้งสถานะตาม R1-R6 แล้ว POST /jobs/{id}/cancel ตรวจสถานะและยอดคืน; R3 ต้องตอบ 409 ตาม ASM-11 |
| AC-07-04 (หน้าจอ) | AC-07-04.test.jsx | API จำลองตอบ 409 พร้อม alternatives 2 ช่วง ตรวจว่าหน้าจอแสดง "ช่วงเวลาถูกจองแล้ว" และปุ่ม 2 ปุ่ม |

หลักแยก: AC ที่ Then บอกว่า "บันทึก" หรือ "สถานะ" ตรวจที่หลังบ้าน AC ที่ Then บอกว่า "แจ้ง" หรือ "เสนอ" ต้องมี test หน้าจอด้วย

## 7. ลำดับงาน

หลังบ้าน
1. ตั้งฐานข้อมูลและตาราง (REQ-DAT-002, REQ-PRV-002, MD-DOM-01)
2. ล็อกช่วงเวลาและหมดอายุ (REQ-FN-041, AS-07)
3. ค้นช่างว่างและตรวจระยะ/การซ้อน (REQ-FN-008, BR-02, BR-03, IF-03, AC-07-02)
4. POST /bookings สร้างงานและ authorize/capture (REQ-FN-008, REQ-IF-001, AC-07-01, AC-07-04, ASM-08)
5. timeout, status-inquiry และกรณีชำระไม่สำเร็จ (REQ-IF-005, AC-07-05, AC-07-06, AC-07-07, ASM-09)
6. คืนมัดจำทุกแถว BR-01 รวม R3 ตาม ASM-11 (REQ-BR-001, AC-07-10)
7. คิวแจ้งเตือนลูกค้าและช่าง (REQ-FN-012, IF-02, AC-07-03, ASM-10)
8. มุมมองช่าง, กรอง log และ retention ประวัติ (REQ-SEC-004, REQ-PRV-002, REQ-DAT-002, AC-07-09, ASM-13, ASM-15)
9. ทดสอบประสิทธิภาพแบบย่อส่วนและสร้าง/เชื่อมหน้าจอ (REQ-QA-003, AC-07-08, AC-07-04)

หน้าจอ (ใช้ API จำลองตามสัญญาข้อ 4 จึงเริ่มพร้อมหลังบ้านได้)
10. หน้าเลือกช่าง หน้ายืนยัน หน้าผล และต่อ API จริง (REQ-FN-008, REQ-FN-041, AC-07-04 หน้าจอ)

## 8. สิ่งที่ยังไม่ทำ

- Q-05: จองโดยไม่ลงทะเบียนยังไม่ตัดสิน; ส่วนที่เกี่ยวข้องกับการจองโดยไม่ลงทะเบียนจะยังไม่สร้างจนกว่าจะได้คำตอบ
