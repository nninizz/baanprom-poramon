"""AC-07-08 แบบย่อส่วน (T-09) ย่อจากผู้ใช้ 500 คน เป็น 20 คำขอพร้อมกัน (บันทึกใน ac-results.md)
ฉบับวัดได้จริงรอ CR-02 (quality-requirements.md) ผลบนเครื่องนักศึกษาเป็นเพียงสัญญาณ ไม่ใช่ผลตรวจรับจริง"""
import asyncio
import threading
import time
import httpx
from sqlalchemy.orm import sessionmaker

from app.db import session as db_session
from app.db.migrations.m001_init import upgrade
from app.db.models import Customer, ServiceAddress, Technician, TimeSlot
from app.db.session import get_db
from app.main import app
from tests.conftest import NOW


# รองรับ AC-07-08 (REQ-QA-003) ฉบับย่อส่วน
def test_AC_07_08_search_under_load_scaled(client, db, seed, tmp_path):
    # รองรับ REQ-QA-003 และ ASM-12: ใช้ file SQLite แยก connection เพื่อจำลอง concurrent requests ได้จริง
    load_engine = db_session.make_engine(f"sqlite:///{tmp_path / 'load-test.db'}")
    upgrade(load_engine)
    LoadSession = sessionmaker(bind=load_engine, autoflush=False, expire_on_commit=False)
    load_db = LoadSession()
    customer = Customer(name=seed["somchai"].name, phone=seed["somchai"].phone)
    technician = Technician(name=seed["prasit"].name, skills=seed["prasit"].skills,
                            base_lat=seed["prasit"].base_lat, base_lng=seed["prasit"].base_lng)
    load_db.add_all([customer, technician])
    load_db.flush()
    address = ServiceAddress(customer_id=customer.id, text=seed["addr"].text,
                             lat=seed["addr"].lat, lng=seed["addr"].lng)
    load_db.add(address)
    load_db.flush()
    for source_slot in seed["slots"]:
        load_db.add(TimeSlot(technician_id=technician.id, start=source_slot.start, end=source_slot.end))
    load_db.commit()
    load_db.close()

    database_lock = threading.Lock()

    def override_db():
        with database_lock:
            request_db = LoadSession()
            try:
                yield request_db
            finally:
                request_db.close()

    app.dependency_overrides[get_db] = override_db
    url = f"/technicians?category=ประปา&address_id={seed['addr'].id}&now={NOW.isoformat()}"

    try:
        # ใช้ customer/address id ของฐานข้อมูล load แทน fixture in-memory
        url = f"/technicians?category=ประปา&address_id={address.id}&customer_id={customer.id}&now={NOW.isoformat()}"

        async def timed_get(index):
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as request_client:
                t0 = time.perf_counter()
                r = await request_client.get(url)
                return r.status_code == 200, time.perf_counter() - t0

        async def run_load():
            return await asyncio.gather(*(timed_get(index) for index in range(20)))

        # Given ลูกค้า 20 คน (ย่อจาก 500) ส่งคำขอค้นหาช่างพร้อมกัน
        results = asyncio.run(run_load())

        # Then ทุกคำขอได้รายการช่างครบ
        assert all(ok for ok, _ in results)
        # Then 19 ใน 20 (ย่อจาก 95 ใน 100) ใช้เวลาไม่เกิน 2 วินาที
        fast = [sec for _, sec in results if sec <= 2.0]
        assert len(fast) >= 19
    finally:
        app.dependency_overrides.pop(get_db, None)
