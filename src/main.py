from fastapi import FastAPI, HTTPException

from src.models import IngestBatchRequest, IngestBatchResponse, IngestedRecord
from src.storage import store

app = FastAPI(
    title="CloudForge Ingest API",
    version="0.2.0",
    description="Ingest Studio API - รับข้อมูล asset เข้าสู่ CloudForge Platform",
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "ingest.ai", "status": "running", "records_stored": store.count()}


@app.post("/ingest", response_model=IngestBatchResponse, status_code=201)
def ingest_batch(request: IngestBatchRequest) -> IngestBatchResponse:
    """
    รับ asset records เข้ามาเป็น batch, บันทึกพร้อม hash สำหรับ traceability
    แล้วคืนผลลัพธ์ว่า record ไหนสำเร็จ/ไม่สำเร็จ
    """
    ingested: list[IngestedRecord] = []
    errors: list[str] = []

    for i, record in enumerate(request.records):
        try:
            ingested.append(store.save(record))
        except Exception as exc:  # กันไม่ให้ record เดียวพังทั้ง batch
            errors.append(f"record[{i}] ({record.external_id}): {exc}")

    return IngestBatchResponse(
        accepted=len(ingested),
        rejected=len(errors),
        records=ingested,
        errors=errors,
    )


@app.get("/ingest/{ingest_id}", response_model=IngestedRecord)
def get_ingested_record(ingest_id: str) -> IngestedRecord:
    record = store.get(ingest_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"ไม่พบ ingest_id: {ingest_id}")
    return record


@app.get("/ingest", response_model=list[IngestedRecord])
def list_ingested_records() -> list[IngestedRecord]:
    return store.list_all()
