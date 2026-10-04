# prompt-log.md บันทึกการใช้ AI ของกลุ่ม X

กติกา: เพิ่มต่อท้ายเท่านั้น ห้ามแก้หรือลบบันทึกเดิม ทุกบันทึกมี เลขที่ | วันที่ | เครื่องมือ | คำสั่ง | สิ่งที่ AI ถามหรือรายงาน | คำตอบหรือการตัดสินใจของทีม | สิ่งที่ AI เดา (ถ้ามี)
บันทึก #1 ถึง #19 อยู่ในบทเรียนก่อนหน้า (ร่าง spec v1, matrix, baseline) คัดเฉพาะหัวข้อไว้ตอนต้น

## บันทึกจากบทเรียนก่อนหน้า (สรุป)

- #12 ถึง #15 (6 ก.ย.) ร่าง spec ส่วน 4 ถึง 6 จาก UC-07 + catalogue ด้วย prompt "บรรณาธิการสเปก" AI เดา 2 อย่างแล้วถูกตัด: ระยะล็อก 15 นาที, สถานะ "รอรีวิว"
- #16 ถึง #19 (6 ก.ย.) ร่างโครง RTM และ Baseline B1 ทีมตรวจและลงชื่อ

## #20 | 4 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /clarify specs/002-booking/spec.md

AI รายงาน 3 ส่วน
A จุดที่กำกวม (7 ข้อ)
1. REQ-FN-041 "ชั่วคราว" คือกี่นาที  ทีม: รู้ เพราะ EV-041 ฝ่ายปฏิบัติการบอก 10 นาที (ปากเปล่า) -> ใส่ใน v2 และคง Q-18 ขอยืนยันเป็นลายลักษณ์อักษร
2. "ช่างที่ว่างใน 7 วัน" นับรวมวันนี้ไหม  ทีม: ไม่รู้ ตัดสินใจเอง ไม่รวมวันนี้ -> AS-06
3. ถ้าลูกค้าปิดเบราว์เซอร์ระหว่างล็อก ใครปลดล็อก  ทีม: ไม่รู้ ต้องถามเจ้าของ -> Q-23 พฤติกรรมชั่วคราว หมดอายุเอง AS-07
4. gateway-timeout 30 วินาทีใน spec ข้อ 9 กับ 60 วินาทีใน Interface Contract IF-01 (docs/srs) อันไหนถูก  ทีม: ไม่รู้ ต้องถาม Dev lead (Q-19) ชั่วคราวใช้ spec = 30
5. AC-07-04 "ใกล้เคียง" กี่ชั่วโมง  ทีม: ไม่รู้ ตอนนั้นตอบว่ารอดูตอน implement (ผิดพลาด ควรตอบตั้งแต่ตอนนี้ ดู GAP-05)
6. BR-01 R3 รอ Q-14 ให้ทำอย่างไร  ทีม: รู้ spec ข้อ 9 มีพฤติกรรมชั่วคราว "ไม่อนุญาต"
7. REQ-QA-003 วัดที่หน้าจอหรือที่ API  ทีม: ไม่รู้ ต้องถามเจ้าของ -> ต่อมากลายเป็น GAP-08 และ CR-02
B สมมติฐานที่ซ่อนอยู่: ลูกค้าหนึ่งคนล็อกได้ทีละ 1 ช่วง (ทีมรับเป็น AS-07 ส่วนหนึ่ง)
C สิ่งที่อยากเดาแต่ไม่ได้เดา: ส่ง SMS ซ้ำ 3 ครั้งถ้าส่งไม่สำเร็จ (ไม่มี REQ รองรับ ไม่ใส่)
ผล: spec.md v2 (Change Log 1.1) commit "spec v2"

## #21 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /plan specs/002-booking/spec.md

AI หยุดถามก่อนเขียนไฟล์: spec ไม่ระบุภาษา framework ฐานข้อมูล เสนอ 3 ชุด (ก) Python FastAPI + React, (ข) Node Express + React, (ค) Django ครบชุด พร้อมข้อดีข้อเสีย
ทีม: เลือก (ก) Python FastAPI + SQLAlchemy + PostgreSQL หลังบ้าน และ React (Vite) + Tailwind CSS หน้าจอ เพราะสมาชิก 3 ใน 4 เคยใช้ และวิชาอื่นใช้ PostgreSQL อยู่แล้ว (บันทึกใน plan.md ข้อ 2 ว่า "ทีมเลือกเอง ไม่ได้มาจาก spec")
AI รายงาน 3 เรื่อง
1. Constraint ที่ยังไม่ได้ใช้: REQ-IF-005 รอ Q-19 (ต่อมาทีมแก้ตารางข้อ 5 เป็น "ใช้แล้ว" เมื่อตั้งค่าชั่วคราว 30)
2. AC ที่ทดสอบยาก: AC-07-08 ต้องการผู้ใช้ 500 คน เสนอย่อส่วนเป็น 20 คำขอ ทีมต้องตัดสินใจ
3. สิ่งที่อยากเดาแต่ไม่ได้เดา: ใช้ Redis เป็นคิว (ไม่อยู่ใน Constraints จึงเขียน "ทีมเลือกเอง" และใช้คิวในหน่วยความจำก่อน)
ทีมเทียบกับแผนที่เขียนเอง (plan-compare.md) พบว่าแผนของทีมลืม REQ-SEC-004 -> GAP-02
ผล: plan.md v1 commit "plan v1"

## #22 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /tasks specs/002-booking/spec.md

AI รายงาน: 11 task, 0 รอ Q | task ยากสุด T-05 (timeout + inquiry) | AC ทดสอบยาก AC-07-08
ทีมตรวจตารางความครบ พบ AC-07-08 "ว่าง" -> สั่ง "เพิ่ม task สำหรับ AC-07-08" ได้ T-09
ทีมพบ T-06 ตั้ง "พร้อมทำ" ทั้งที่ R3 รอ Q-14 -> GAP-03
แก้รอบที่ 1: สั่ง "T-06 ทำเฉพาะ R1, R2, R4, R5, R6 ส่วน R3 ใช้พฤติกรรมชั่วคราวตาม spec ข้อ 9 และข้าม test R3 พร้อมเหตุผล" AI แก้แล้ว
ผล: tasks.md v1 commit "tasks v1"

## #23 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /implement T-01 specs/002-booking/tasks.md

AI ตรวจ 3 อย่างก่อนเริ่ม ผ่าน repo ยังไม่มีโค้ด จึงสร้างโครงตาม plan.md ข้อ 2 ก่อน (backend/requirements.txt, pytest.ini, frontend/package.json, vite.config.js) แล้วสร้าง config.py, session.py, models.py, m001_init.py, main.py, conftest.py
ตรวจ 5 ข้อ: ข้อ 1 ไฟล์ที่แตะ **ไม่ตรง** AI แก้ booking/router.py เพิ่มด้วย (ไฟล์ของ T-04) -> GAP-04 สั่ง revert แล้วทำใหม่
สิ่งที่ AI ถามแทนการเดา: จะเก็บ job_status_history แยกตารางหรือเก็บใน jobs  ทีม: แยกตาราง (REQ-DAT-002 ต้องเก็บประวัติ 24 เดือน)
test: test พื้นฐานสร้างตาราง 8 ตาราง ผ่าน

## #24 | 4 ต.ค. 2569 | /implement T-02

สร้าง hold_slot, release_expired_holds, POST /slots/{id}/hold  ผ่านตรวจ 5 ข้อ
AI ถาม: ลูกค้าคนเดิมล็อกซ้ำช่วงเดิมได้ไหม  ทีม: ได้ ต่ออายุให้ (บันทึกเป็นพฤติกรรม ไม่ต้องมี REQ ใหม่เพราะไม่ขัดกับ REQ-FN-041)

## #25 | 4 ต.ค. 2569 | /implement T-03

สร้าง technicians/service.py, router.py, clock.py และ test_AC_07_02 ผ่าน
AI ถาม: ระยะทาง BR-03 คำนวณอย่างไรเมื่อยังไม่มี IF-03 จริง  ทีม: ใช้สูตร haversine ชั่วคราว ใส่คอมเมนต์ว่า IF-03 ในระบบจริง
AI เพิ่ม now=... ใน query เพื่อให้ test กำหนดเวลาได้ ทีมรับ แต่กำกับว่าระบบจริงไม่รับค่านี้ (ต้องมี task ปิดก่อนขึ้นระบบจริง ยังไม่สร้างเพราะไม่มี REQ รองรับ -> จดไว้ใน README)

## #26 | 4 ต.ค. 2569 | /implement T-04

AI หยุดถาม: AC-07-04 "ใกล้เคียง" กี่ชั่วโมง เขียน assert ไม่ได้  ทีม: ไม่รู้ -> เปิด CR-01 (3 ชั่วโมง ที่มา EV-004) RE lead อนุมัติ แก้ spec v3 และ booking.feature v1.1 ก่อน แล้วสั่งทำต่อ (GAP-05)
สร้าง create_booking, payments/gateway.py, payments/service.py, POST /bookings  test_AC_07_01, test_AC_07_04 ผ่าน
ตรวจ 5 ข้อ: ข้อ 4 test ตรวจ Then ครบไหม พบ test_AC_07_01 ไม่ได้นับจำนวน Payment (ทดลองให้ตัดเงิน 2 ครั้ง test ยังผ่าน) -> GAP-06 สั่งเพิ่ม assert

## #27 | 4 ต.ค. 2569 | /implement T-05

สร้าง GatewayTimeout, status_inquiry, test_payment.py
pytest รอบแรก: test_AC_07_05 **ไม่ผ่าน** assert timeout 30 แต่ AI ตั้ง GATEWAY_TIMEOUT_SECONDS = 60 ตาม IF-01 ใน docs/srs
AI รายงานว่า "เอกสารสองฉบับบอกไม่ตรงกัน ไม่เดา" ทีม: spec.md ข้อ 9 ชนะ (30) ตั้ง config 30 -> GAP-07 บันทึกให้ Dev lead เช็คสัญญาจริง (Q-19)
รอบสอง test_AC_07_05, 06, 07 ผ่าน

## #28 | 4 ต.ค. 2569 | /implement T-06

AI ตรวจก่อนเริ่ม: T-06 มีหมายเหตุ R3 รอ Q-14 ถามว่าจะทำต่อไหม ทีม: ทำตามแก้รอบที่ 1 (เฉพาะแถวอื่น R3 ตอบ 409)
สร้าง refund/rules.py, service.py, router.py, test_refund.py  ผ่าน 5 แถว + R6 + R3 ชั่วคราว, R3 ข้าม
AI ถาม: "ปัดขึ้นหลักสิบ" ของ 175 คือ 180 ใช่ไหม  ทีม: ใช่ ตาม rules.md ตัวอย่าง

## #29 | 4 ต.ค. 2569 | /implement T-07

สร้าง notify/queue.py, enqueue ใน create_booking, GET /notifications/queue  test_AC_07_03 ผ่าน
AI ไม่ได้ถามอะไร ไม่มีการเดา

## #30 | 4 ต.ค. 2569 | /implement T-08

สร้าง technician_view, GET /jobs/{id}/technician-view, privacy.py, test_privacy.py
ตรวจ 5 ข้อ: ข้อ 3 Constraint เห็นในโค้ดจริงไหม พบ router log ทั้ง dict รวมเบอร์โทร (ขัด REQ-PRV-002) -> GAP-09 สั่งให้ทุก logger ผ่าน privacy.py และเพิ่ม assert ใน test
พิสูจน์ชั้น 3: เปลี่ยน PHONE_REVEAL_HOURS เป็น 3 test พัง เปลี่ยนกลับ test ผ่าน

## #31 | 4 ต.ค. 2569 | /implement T-09

AI บอกว่า AC-07-08 ทดสอบจริงไม่ได้ในสภาพแวดล้อมนี้ เสนอ test ย่อส่วน 20 คำขอ ทีม: รับ แต่ต้องบันทึกใน ac-results.md ว่าย่อส่วน และเปิด CR-02 ให้สเปกวัดได้ (GAP-08)
สร้าง test_load_scaled.py ผ่าน

## #32 | 4 ต.ค. 2569 | /implement T-10

สร้างหน้าจอ 3 หน้าและ AC-07-04.test.jsx
npm test รอบแรกพัง: toHaveTextContent ไม่รู้จัก (ไม่มี jest-dom ใน template) -> GAP-10 สาเหตุ env AI เสนอเพิ่ม @testing-library/jest-dom ทีมอนุมัติ (แตะ package.json, vite.config.js, setupTests.js นอกรายการไฟล์เดิม ทีมเพิ่มในช่อง "ไฟล์ที่แตะ" ของ T-10 ก่อนให้ทำ)
AI ถาม: ยอดมัดจำบนหน้าจอเอาจากไหนก่อนจอง  ทีม: ใช้ตารางเดียวกับหลังบ้าน (ประปา 350) ชั่วคราว ระบบจริงต้องมี API ราคาประเมิน (UC-07 ขั้น 4 ยังไม่มี REQ แยก จดไว้)

## #33 | 4 ต.ค. 2569 | /implement T-11

เพิ่ม seed_demo.py และยืนยัน proxy /api ใน vite.config.js เปิด uvicorn + npm run dev กดจองจนเห็น "งาน #1 สถานะ ยืนยันแล้ว"
ไม่มีการเดา

## #34 | 4 ต.ค. 2569 | รัน test ทั้งชุด

cd backend && pytest -v -k "AC_" 2>&1 | tee ../specs/002-booking/test-run.txt  ผล 15 passed, 1 skipped
cd frontend && npm test  ผล 1 passed
กรอก ac-results.md รอบที่ 2 และสรุป gaps.md 10 แถว

## #35 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /clarify specs/002-booking/spec.md (ตอบกลับ)

คำสั่งของทีม: "เอาตามที่เดาเลย"

AI ถาม 8 ข้อเกี่ยวกับพฤติกรรมเมื่อ Payment Gateway และระบบส่งข้อความไม่ตอบ, ความหมายของการชำระสำเร็จ, BR-01 R3, ช่วง 7 วันและระยะ 15 กิโลเมตร, วิธีวัด REQ-QA-003, ขอบเขตการเปิดเผยเบอร์ และการจัดการประวัติครบ 24 เดือน

คำตอบหรือการตัดสินใจของทีม: ให้ใช้สมมติฐานตามที่ AI ระบุทั้งหมด

สิ่งที่แก้ใน specs/002-booking/spec.md: เปลี่ยนสถานะเป็น Draft v2; ระบุเงื่อนไข capture, gateway timeout และ status-inquiry; กำหนดพฤติกรรมการแจ้งเตือน; ยืนยัน R3; ระบุขอบเขต 7 วัน ระยะ 15 กิโลเมตร และการวัด p95; ระบุขอบเขตการเปิดเผยเบอร์และการลบประวัติ; แปลง Q-14, Q-18, Q-19, Q-22, Q-23 เป็น ASM-08 ถึง ASM-15; อัปเดต Change Log, Requirements, Acceptance Criteria, Data และ Decision Log

## #36 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /plan specs/002-booking/spec.md

ผลลัพธ์: ปรับ specs/002-booking/plan.md จาก plan เดิมให้ตรงกับ spec.md v1.3 Draft v2 โดยยังไม่เขียนโค้ด

สิ่งที่ทำ: อัปเดตสรุปแนวทางและเทคโนโลยีโดยระบุรายการที่ทีมเลือกเอง; ระบุโครงโฟลเดอร์ ไฟล์ติดตั้ง และคำสั่งรัน test; ปรับโมเดลข้อมูลและ API ให้รองรับ ASM-08 ถึง ASM-15; เติมตารางตรวจ REQ-CON-001, REQ-CON-003, IF-01 ถึง IF-03 และ MD-CTX-01, MD-DOM-01, MD-STM-01, MD-SEQ-07-05; ทำตารางทดสอบครบ AC-07-01 ถึง AC-07-10; จัดลำดับงาน 10 ขั้น; คัดลอก Q-05 ไว้ในหัวข้อสิ่งที่ยังไม่ทำ

ข้อจำกัดที่ยังไม่ได้ใช้: ไม่มี Constraint หรือ IF ที่ยังไม่ได้ใช้ใน plan; Q-05 เป็น Open Question ของ non-goal ไม่ใช่ Constraint และไม่สร้างส่วนที่เกี่ยวข้อง

AC ที่ทดสอบยาก: AC-07-08 ยังใช้การทดสอบย่อส่วน 20 คำขอแทนผู้ใช้พร้อมกัน 500 คน และต้องรายงานข้อจำกัดของสภาพแวดล้อม

สิ่งที่ AI อยากเดาแต่ไม่ได้เดา: พฤติกรรมการจองโดยไม่ลงทะเบียนตาม Q-05 จะยังไม่สร้างจนกว่าทีมจะตัดสินใจ

## #37 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /tasks specs/002-booking/spec.md

ผลลัพธ์: สร้าง specs/002-booking/tasks.md ใหม่จาก spec.md v1.3 Draft v2 และ plan.md โดยยังไม่เริ่มทำ task ใด

สรุป: 12 task และ 0 task รอ Q-xx; ทุก task อยู่ในสถานะ "พร้อมทำ"

สิ่งที่ทำ: แยกงานตาม dependency ตั้งแต่โครง/โมเดล, hold, ค้นช่าง, booking/payment, timeout/status-inquiry, refund, notification, privacy, load test และ frontend; ทำตารางตรวจ AC-07-01 ถึง AC-07-10 ครบ; ทำตารางตรวจ REQ-CON-001, REQ-CON-003, IF-01 ถึง IF-03 และ model/context IDs ครบ; คัดลอก Q-05 ไว้ในหัวข้อสิ่งที่ยังไม่ทำโดยไม่สร้าง task ให้พฤติกรรมนอกขอบเขต

task ที่ยากที่สุด: T-06 เพราะต้องคุมลำดับ authorize, status-inquiry, capture, ผล unknown/approved และการไม่ตัดเงินซ้ำ

AC ที่ทดสอบยาก: AC-07-08 ต้องการผู้ใช้พร้อมกัน 500 คน จึงกำหนด T-10 ให้ทดสอบย่อส่วน 20 คำขอและบันทึกข้อจำกัดไว้ โดยไม่ถือเป็นผลตรวจรับจริง

## #38 | 4 ต.ค. 2569 | Copilot Chat (Agent) | แก้ tasks.md: เพิ่ม Safe implementation note

ทีมขอ: "ทำ safe implementation note"

สิ่งที่แก้: เพิ่มหัวข้อ Safe implementation note ใน specs/002-booking/tasks.md โดยกำหนดขอบเขตไม่ให้สร้างเส้นทางจองโดยไม่ลงทะเบียนตาม Q-05; ย้ำลำดับ capture และการใช้ gatewayRef เดิม; ย้ำ R3 ต้องตอบ 409 และไม่คืนมัดจำ; ป้องกัน retry notification สร้าง Job หรือ Payment ซ้ำ; และห้าม log Customer.phone ตาม REQ-PRV-002

## #40 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /implement T-11 specs/002-booking/tasks.md

ไฟล์ที่สร้างหรือแก้: specs/002-booking/tasks.md

ผลการทำงาน: ตรวจพบว่า frontend implementation และ test ของ T-11 มีอยู่แล้วตรงตาม plan; ไม่แก้ source frontend เพื่อไม่เปลี่ยนไฟล์เกินความจำเป็น; เปลี่ยนสถานะ T-11 เป็น "เสร็จ รอทีมตรวจ"

ผล test: `cd frontend && npm test -- --run src/__tests__/AC-07-04.test.jsx` ผ่าน 1 test และ 1 test suite ใน 3.39 วินาที

สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่พบสิ่งที่ต้องเดาเพิ่ม; test ใช้ API จำลองตามสัญญาใน plan และไม่เริ่ม T-12

## #41 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /implement T-02 specs/002-booking/tasks.md

ไฟล์ที่สร้างหรือแก้: backend/app/db/models.py, specs/002-booking/tasks.md

ผลการทำงาน: เพิ่ม `status_history_cutoff` สำหรับเส้นตัดย้อนหลัง 24 เดือนปฏิทิน และ `purge_status_history` ที่ลบเฉพาะประวัติเก่ากว่าเส้นตัด; ใช้ `set_status` เดิมบันทึก job_status_history; เปลี่ยนสถานะ T-02 เป็น "เสร็จ รอทีมตรวจ"

ผล test: focused SQLite check ผ่าน โดยยืนยันการบันทึก status history และลบรายการเก่า 1 รายการ พร้อมคงรายการที่อยู่ตรงเส้น 24 เดือนไว้

สิ่งที่เกือบต้องเดาแต่ถามแทน: spec ไม่ระบุจังหวะเรียก purge จึงไม่เพิ่ม startup trigger ใน main.py และไม่เปลี่ยน migration ที่ไม่มี schema ใหม่

## #39 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /implement T-01 specs/002-booking/tasks.md

ไฟล์ที่สร้างหรือแก้: backend/app/config.py, backend/app/db/models.py, specs/002-booking/tasks.md

ผลการทำงาน: ตรวจโครงโปรเจกต์และ schema ตาม plan; เพิ่ม `Payment.captured_at` ให้ตรงกับโมเดลใน plan และปรับคำอธิบาย HOLD_MINUTES/GATEWAY_TIMEOUT_SECONDS จาก Q-18/Q-19 เป็น ASM-08/ASM-09; เปลี่ยนสถานะ T-01 เป็น "เสร็จ รอทีมตรวจ"

ผล test: `cd backend && pytest -q tests/test_booking.py tests/test_payment.py` ผ่าน 7 passed, 1 warning; schema check ผ่าน 8 ตารางและตรวจพบคอลัมน์ `captured_at`

สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่พบข้อมูลที่ต้องเดาเพิ่ม; full suite มี failure เดิมใน `tests/test_load_scaled.py` ซึ่งอยู่นอกขอบเขตไฟล์ของ T-01 จึงไม่แก้ใน task นี้
