# CloudForge Ingest Studio

Studio ตัวแรกของ CloudForge Platform — พิสูจน์ pipeline end-to-end ก่อนไล่สร้าง
Knowledge → Nova → Security → Compliance

## Local Dev

```bash
docker compose up --build
```

- API: http://localhost:8000
- Health check: http://localhost:8000/healthz

## Governance / Foundation Validation

Workflow `.github/workflows/validate-against-foundation.yml` เรียกผ่าน
`niphan1000-cyber1000/foundation-validation/.github/workflows/reusable-gate.yml@v1`

**ต้องตั้งก่อนใช้งานจริง:**
1. เพิ่ม repo secret `FOUNDATION_PAT` (PAT ที่มีสิทธิ์อ่าน
   `CloudForge-Platform-Foundation` และ `foundation-validation`)
2. ยืนยันว่า `openapi.yaml` มี `x-owner` ตามกฎ Foundation `.spectral.yaml`

> ⚠️ Workflow นี้ syntax valid และผ่านการตรวจแล้ว แต่ **ยังไม่เคยรันจริงกับ
> Studio repo จริงมาก่อน** — นี่คือ Studio ตัวแรกที่ใช้ทดสอบ end-to-end
> ถ้ามี error ให้เช็ค:
> - secret `FOUNDATION_PAT` ตั้งถูกไหม
> - `spec_path` output จาก `detect-openapi-spec` ตรงกับ path จริงไหม
> - engine version (`v1`) ยัง compatible กับ policy ฝั่ง Foundation ไหม

## Local Validation (ไม่ต้องรอ CI) — ทำทีหลัง (ขั้นตอน 3 ตามแผน)

จะเพิ่ม image `foundation-validation` ให้รันตรวจ local ได้ ตอนนี้ยังไม่ทำ
ตามลำดับที่วางไว้ (เริ่มแค่ API ใน Docker + validation ผ่าน reusable workflow ก่อน)

## Roadmap ของโปรเจกต์ (ลำดับ Studio)

1. **Ingest** ← ตอนนี้ (พิสูจน์ pipeline + ส่งข้อมูลเข้า)
2. Knowledge ← ใช้ข้อมูลจาก Ingest
3. Nova ← ออกแบบ/architecture บนข้อมูลที่มี
4. Security ← วิเคราะห์ความปลอดภัยของระบบที่มีแล้ว
5. Compliance ← ชั้นบนสุด อาศัยทุกตัวก่อนหน้า
