from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    """ประเภทของ asset ที่รับเข้ามา migrate"""

    VM = "vm"
    DATABASE = "database"
    STORAGE_BUCKET = "storage_bucket"
    NETWORK_CONFIG = "network_config"
    APPLICATION = "application"


class AssetRecord(BaseModel):
    """หนึ่งรายการ asset ที่ต้องการ ingest เข้าระบบ"""

    source_system: str = Field(..., min_length=1, description="ระบบต้นทาง เช่น 'aws-prod', 'on-prem-vsphere'")
    asset_type: AssetType
    external_id: str = Field(..., min_length=1, description="ID ของ asset ในระบบต้นทาง")
    payload: dict[str, Any] = Field(default_factory=dict, description="ข้อมูลดิบของ asset")


class IngestBatchRequest(BaseModel):
    """คำขอ ingest ทีเดียวหลาย record"""

    records: list[AssetRecord] = Field(..., min_length=1, max_length=1000)


class IngestedRecord(BaseModel):
    """record ที่ถูกบันทึกแล้ว พร้อม metadata สำหรับ traceability"""

    ingest_id: str
    source_system: str
    asset_type: AssetType
    external_id: str
    content_hash: str
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IngestBatchResponse(BaseModel):
    """ผลลัพธ์หลัง ingest batch เสร็จ"""

    accepted: int
    rejected: int
    records: list[IngestedRecord]
    errors: list[str] = Field(default_factory=list)
