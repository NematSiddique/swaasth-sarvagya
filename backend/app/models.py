from datetime import UTC, datetime
from datetime import date as date_type

from pydantic import EmailStr
from sqlalchemy import JSON, Column, DateTime, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


# SwaasthSarvagya AI domain models


class Hospital(SQLModel):
    __tablename__ = "hospitals"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    district: str
    type: str = Field(max_length=50)
    latitude: float | None = None
    longitude: float | None = None
    total_beds: int
    created_at: datetime


class Disease(SQLModel):
    __tablename__ = "diseases"

    id: int | None = Field(default=None, primary_key=True)
    disease_name: str
    category: str | None = None
    seasonal: bool
    description: str | None = None
    seasonal_trends: dict | None = None
    weather_correlation: dict | None = None
    demographic_risk: dict | None = None


class MedicineGroup(SQLModel):
    __tablename__ = "medicine_groups"

    id: int | None = Field(default=None, primary_key=True)
    group_name: str


class Medicine(SQLModel):
    __tablename__ = "medicines"

    id: int | None = Field(default=None, primary_key=True)
    group_id: int | None = None
    generic_name: str
    brand_name: str | None = None
    dosage: str | None = None


class DiseaseMedicine(SQLModel):
    __tablename__ = "disease_medicines"

    disease_id: int = Field(foreign_key="diseases.id", primary_key=True)
    medicine_id: int = Field(foreign_key="medicines.id", primary_key=True)
    priority: int


class Doctor(SQLModel):
    __tablename__ = "doctors"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    name: str
    specialization: str | None = None
    shift: str | None = None
    leave_status: str | None = None
    consultation_count: int


class Nurse(SQLModel):
    __tablename__ = "nurses"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    name: str
    shift: str | None = None
    attendance_status: str | None = None
    leave_status: str | None = None


class DoctorAttendance(SQLModel):
    __tablename__ = "doctor_attendance"

    doctor_id: int = Field(foreign_key="doctors.id", primary_key=True)
    date: date_type = Field(primary_key=True)
    status: bool
    hours_worked: float | None = None


class Patient(SQLModel):
    __tablename__ = "patients"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    doctor_id: int | None = None
    disease_id: int | None = None
    age: int | None = None
    gender: str | None = None
    severity: str | None = None
    bed_required: bool
    bed_allocated: bool
    admission_status: str | None = None
    registered_at: datetime
    discharged_at: datetime | None = None


class Laboratory(SQLModel):
    __tablename__ = "laboratories"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    name: str
    status: str | None = None


class LabEquipment(SQLModel):
    __tablename__ = "lab_equipment"

    id: int | None = Field(default=None, primary_key=True)
    laboratory_id: int
    equipment_name: str
    status: str
    last_service: date_type | None = None
    expected_life: int | None = None
    usage_frequency: int | None = None
    machine_age: int | None = None


class LabKit(SQLModel):
    __tablename__ = "lab_kits"

    id: int | None = Field(default=None, primary_key=True)
    laboratory_id: int
    test_name: str
    stock: int
    threshold: int


class DiseaseTest(SQLModel):
    __tablename__ = "disease_tests"

    disease_id: int = Field(foreign_key="diseases.id", primary_key=True)
    test_name: str = Field(primary_key=True)
    priority: int


class Bed(SQLModel):
    __tablename__ = "beds"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    bed_type: str
    occupied: bool
    patient_id: int | None = None


class Inventory(SQLModel):
    __tablename__ = "inventory"
    __table_args__ = (
        UniqueConstraint(
            "hospital_id", "medicine_id", name="uq_inventory_hospital_medicine"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    medicine_id: int
    quantity: int
    expiry_date: date_type | None = None
    reorder_level: int
    updated_at: datetime


class InventoryTransaction(SQLModel):
    __tablename__ = "inventory_transactions"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    medicine_id: int
    quantity: int
    transaction_type: str
    source_hospital_id: int | None = None
    destination_hospital_id: int | None = None
    timestamp: datetime


class Supplier(SQLModel):
    __tablename__ = "suppliers"

    id: int | None = Field(default=None, primary_key=True)
    supplier_name: str
    delivery_days: int | None = None
    reliability: float | None = None
    contact: str | None = None
    active_orders: int


class SupplierMedicine(SQLModel):
    __tablename__ = "supplier_medicines"

    supplier_id: int = Field(foreign_key="suppliers.id", primary_key=True)
    medicine_id: int = Field(foreign_key="medicines.id", primary_key=True)


class PatientTest(SQLModel):
    __tablename__ = "patient_tests"

    patient_id: int = Field(foreign_key="patients.id", primary_key=True)
    test_name: str = Field(primary_key=True)
    status: str
    ordered_at: datetime


class Forecast(SQLModel):
    __tablename__ = "forecasts"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int
    forecast_type: str
    target: str
    predicted_value: float
    confidence: float | None = None
    model_name: str | None = None
    generated_at: datetime
    forecast_for: date_type | None = None


class Alert(SQLModel):
    __tablename__ = "alerts"

    id: int | None = Field(default=None, primary_key=True)
    hospital_id: int | None = None
    alert_type: str
    severity: str
    message: str
    resolved: bool
    created_at: datetime


class Recommendation(SQLModel):
    __tablename__ = "recommendations"

    id: int | None = Field(default=None, primary_key=True)
    alert_id: int | None = None
    recommendation: str
    reason: str | None = None
    priority: int
    accepted: bool
    created_at: datetime


class DailyPatientStats(SQLModel):
    __tablename__ = "daily_patient_stats"

    hospital_id: int = Field(foreign_key="hospitals.id", primary_key=True)
    date: date_type = Field(primary_key=True)
    total_patients: int
    disease_counts: dict | None = None
    admissions: int
    discharges: int


class DailyInventoryUsage(SQLModel):
    __tablename__ = "daily_inventory_usage"

    hospital_id: int = Field(foreign_key="hospitals.id", primary_key=True)
    medicine_id: int = Field(foreign_key="medicines.id", primary_key=True)
    date: date_type = Field(primary_key=True)
    used_today: int
    remaining: int
    forecast: float | None = None


class DailyBedStats(SQLModel):
    __tablename__ = "daily_bed_stats"

    hospital_id: int = Field(foreign_key="hospitals.id", primary_key=True)
    date: date_type = Field(primary_key=True)
    occupied: int
    available: int
    admissions: int
    discharges: int


class DailyDoctorStats(SQLModel):
    __tablename__ = "daily_doctor_stats"

    doctor_id: int = Field(foreign_key="doctors.id", primary_key=True)
    date: date_type = Field(primary_key=True)
    patients_seen: int
    attendance: bool
    hours_worked: float | None = None
