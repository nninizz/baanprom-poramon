# Tasks: การจองงานบริการซ่อมบำรุง (UC-07)

Feature: SPEC-BOOKING | อ้างอิง: plan.md SPEC-BOOKING v1.3 Draft v2 | วันที่: 2569-10-04

สรุป: 12 task | 0 task รอ Q-xx ทั้งหมดเป็นงานที่พร้อมทำตาม ASM-08 ถึง ASM-15

### T-01 ตั้งโครงโปรเจกต์และโมเดลข้อมูล
- รองรับ: REQ-DAT-002, REQ-PRV-002, MD-DOM-01, MD-STM-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 ถึง T-09
- ไฟล์ที่แตะ: backend/requirements.txt, backend/pytest.ini, frontend/package.json, frontend/vite.config.js, backend/app/config.py, backend/app/db/session.py, backend/app/db/models.py, backend/app/db/migrations/m001_init.py, backend/app/main.py, backend/tests/conftest.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: สร้าง/ตรวจโครงตาม plan และรัน test เปล่า 1 ตัวผ่าน พร้อมสร้างตาราง Customer, ServiceAddress, Technician, TimeSlot, Job, job_status_history, Payment และ Refund ได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้างการเก็บประวัติสถานะและ retention
- รองรับ: REQ-DAT-002, ASM-15, MD-STM-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-07 และการตรวจผ่าน T-01
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/m001_init.py, backend/app/main.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: เปลี่ยนสถานะแล้วบันทึก job_status_history และลบประวัติที่เกิน 24 เดือนตาม ASM-15 ได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 ล็อกช่วงเวลาและหมดอายุอัตโนมัติ
- รองรับ: REQ-FN-041, AS-07, ASM-08, BR-02
- ตรวจด้วย: AC-07-04
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/technicians/service.py, backend/app/booking/router.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: POST /slots/{slot_id}/hold ตอบ hold_expires_at = now + 10 นาที และการอ่าน slot หมดอายุ hold อัตโนมัติ; test_AC_07_04_no_charge_when_slot_taken ผ่านส่วนที่เกี่ยวกับ slot
- สถานะ: พร้อมทำ

### T-04 ค้นช่างว่างตามประเภท ระยะทาง และช่วงที่ไม่ซ้อน
- รองรับ: REQ-FN-008, AS-06, BR-02, BR-03, IF-03
- ตรวจด้วย: AC-07-02
- ไฟล์ที่แตะ: backend/app/technicians/service.py, backend/app/technicians/router.py, backend/app/clock.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /technicians แสดงเฉพาะ slot ใน 7 วันถัดไป ไม่ซ้อน และไม่เกิน 15 กิโลเมตร; test_AC_07_02_slot_not_rebookable ผ่าน
- สถานะ: พร้อมทำ

### T-05 สร้างงานและชำระด้วย authorize แล้ว capture
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-CON-003, ASM-08
- ตรวจด้วย: AC-07-01, AC-07-04
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py, backend/app/payments/gateway.py, backend/app/payments/service.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: approved ทำให้เกิด Job confirmed, slot จองแล้ว และ capture สำเร็จเพียงครั้งเดียว; slot ที่ถูกจองก่อนตอบ 409 โดยไม่ตัดเงินซ้ำ และ test_AC_07_01_booking_success กับ test_AC_07_04_no_charge_when_slot_taken ผ่าน
- สถานะ: พร้อมทำ

### T-06 จัดการ gateway timeout และ status-inquiry
- รองรับ: REQ-IF-001, REQ-IF-005, IF-01, MD-SEQ-07-05, ASM-09
- ตรวจด้วย: AC-07-05, AC-07-06, AC-07-07
- ไฟล์ที่แตะ: backend/app/payments/gateway.py, backend/app/payments/service.py, backend/tests/test_payment.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: timeout 30 วินาทีเรียก status-inquiry ด้วย reference เดิมหนึ่งครั้ง; unknown ยกเลิกอัตโนมัติและ approved ยืนยันงานโดยไม่ตัดซ้ำ; test_AC_07_05, test_AC_07_06 และ test_AC_07_07 ผ่าน
- สถานะ: พร้อมทำ

### T-07 คืนมัดจำและยกเลิกงานตาม BR-01
- รองรับ: REQ-BR-001, BR-01, MD-STM-01, ASM-11
- ตรวจด้วย: AC-07-10
- ไฟล์ที่แตะ: backend/app/refund/rules.py, backend/app/refund/service.py, backend/app/refund/router.py, backend/tests/test_refund.py
- ต้องทำหลัง: T-05, T-06
- เสร็จเมื่อ: R1-R6 ให้สถานะและยอดคืนถูกต้อง โดย R3 ตอบ 409 และไม่คืนมัดจำตาม ASM-11; test_AC_07_10_refund_R1_to_R6 ผ่าน
- สถานะ: พร้อมทำ

### T-08 เข้าคิวแจ้งลูกค้าและช่าง
- รองรับ: REQ-FN-012, IF-02, ASM-10
- ตรวจด้วย: AC-07-03
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/app/main.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: สร้างงานแล้วมีข้อความของลูกค้าและช่างในคิวภายใน 60 วินาที และ retry ตาม ASM-10; test_AC_07_03_notify_both_within_60s ผ่าน
- สถานะ: พร้อมทำ

### T-09 จำกัดการเห็นเบอร์และกรอง log
- รองรับ: REQ-SEC-004, REQ-PRV-002, ASM-13
- ตรวจด้วย: AC-07-09
- ไฟล์ที่แตะ: backend/app/privacy.py, backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_privacy.py
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: technician-view ซ่อนเบอร์ก่อน 2 ชั่วโมง เปิดเผยถึงปิดงานตาม ASM-13 และ log ไม่มีเบอร์; test_AC_07_09_phone_hidden_until_2h ผ่าน
- สถานะ: พร้อมทำ

### T-10 ทดสอบประสิทธิภาพแบบย่อส่วน
- รองรับ: REQ-QA-003, ASM-12
- ตรวจด้วย: AC-07-08
- ไฟล์ที่แตะ: backend/tests/test_load_scaled.py, specs/002-booking/ac-results.md
- ต้องทำหลัง: T-04, T-05
- เสร็จเมื่อ: test_AC_07_08_search_under_load_scaled รันการทดสอบ 20 คำขอพร้อมกัน วัดจากค้นหาถึงยืนยันโดยไม่รวม gateway และบันทึกว่าเป็นการย่อส่วนจาก 500 คน
- สถานะ: พร้อมทำ

### T-11 สร้างหน้าจอด้วย API จำลอง
- รองรับ: REQ-FN-008, REQ-FN-041, AC-07-04
- ตรวจด้วย: AC-07-04
- ไฟล์ที่แตะ: frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/pages/TechnicianPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-07-04.test.jsx, frontend/src/setupTests.js, frontend/index.html
- ต้องทำหลัง: ไม่มี (ใช้สัญญา API ใน plan.md ข้อ 4)
- เสร็จเมื่อ: API จำลองตอบ 409 พร้อม alternatives แล้วหน้าจอแสดงช่วงเวลาถูกจองและตัวเลือกใกล้เคียง; AC-07-04.test.jsx ผ่าน
- สถานะ: เสร็จ รอทีมตรวจ

### T-12 ต่อหน้าจอกับ API จริงและตรวจ flow จอง
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-IF-001, IF-01, IF-02, IF-03
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นการตรวจ flow รวมของ T-04, T-05, T-08 และ T-11
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/vite.config.js, backend/seed_demo.py
- ต้องทำหลัง: T-04, T-05, T-08, T-11
- เสร็จเมื่อ: เปิด backend และ frontend แล้วค้นหา เลือก slot ยืนยัน และเห็นงานสถานะ "ยืนยันแล้ว" พร้อมข้อความในคิว
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-07-01 | T-05 |
| AC-07-02 | T-04 |
| AC-07-03 | T-08 |
| AC-07-04 | T-03, T-05, T-11 |
| AC-07-05 | T-06 |
| AC-07-06 | T-06 |
| AC-07-07 | T-06 |
| AC-07-08 | T-10 |
| AC-07-09 | T-09 |
| AC-07-10 | T-07 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-001 | T-12 ไม่รวม A2 ตาม D-07-02 และทุก task อยู่ในขอบเขต R1 |
| REQ-CON-003 | T-05, T-06 และ T-12 ใช้ Gateway interface ของรายเดิม |
| IF-01 | T-05, T-06, T-07 และ T-12 |
| IF-02 | T-08 และ T-12 |
| IF-03 | T-04 และ T-12 |
| MD-CTX-01 | T-04 ถึง T-12 เชื่อม actor และระบบภายนอกตาม context |
| MD-DOM-01 | T-01, T-02 และ T-07 |
| MD-STM-01 | T-01, T-02 และ T-07 |
| MD-SEQ-07-05 | T-05 และ T-06 |
| REQ-PRV-002 | T-01 และ T-09 |
| REQ-SEC-004 | T-09 |
| REQ-DAT-002 | T-01 และ T-02 |

## สิ่งที่ยังไม่ทำ

- Q-05: จองโดยไม่ลงทะเบียนยังไม่ตัดสิน; ไม่มี task สำหรับพฤติกรรมนี้ และจะยังไม่สร้างจนกว่าจะได้คำตอบ

## Safe implementation note

- Q-05: คงการบังคับลงทะเบียนก่อนจองตามพฤติกรรมชั่วคราวของ spec; ห้ามเพิ่ม endpoint, branch หรือ bypass สำหรับผู้ใช้ไม่ลงทะเบียนจนกว่าจะมีคำตอบ
- T-05 และ T-06: ใช้ `gatewayRef` เดิมกับ status-inquiry; ห้ามเปลี่ยนงานเป็น "ยืนยันแล้ว" ก่อน `capture` สำเร็จ และห้ามสร้างรายการชำระซ้ำเมื่อ inquiry ได้ผล `approved`
- T-07: กรณี BR-01 R3 ให้ตอบ 409 และไม่คืนมัดจำตาม ASM-11; อย่าแทนที่ด้วยการเดานโยบายใหม่
- T-08: การ retry แจ้งเตือนต้องทำกับข้อความในคิว ไม่สร้าง Job หรือ Payment ใหม่
- T-09: ห้ามส่ง `Customer.phone` เข้า logger และเปิดเผยเบอร์ตามช่วงเวลาของ ASM-13 เท่านั้น