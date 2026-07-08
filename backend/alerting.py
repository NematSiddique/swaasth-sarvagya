from datetime import datetime, timedelta

from sqlalchemy import String, cast, func
from sqlmodel import Session, col, select

from app.models import (
    Alert,
    Bed,
    Doctor,
    DoctorAttendance,
    Forecast,
    Hospital,
    Inventory,
    LabEquipment,
    LabKit,
    Laboratory,
    Patient,
)

# --- Alerting Thresholds ---
BED_OCCUPANCY_CRITICAL_THRESHOLD = 0.90
FORECASTED_BED_OCCUPANCY_THRESHOLD = 0.85
DISEASE_SPIKE_FACTOR = 2.5  # e.g., 2.5x the recent average
MEDICINE_EXPIRY_WARNING_DAYS = 30
EQUIPMENT_SERVICE_INTERVAL_MONTHS = 6


def _create_alert_if_not_exists(
    db: Session, *, hospital_id: int, alert_type: str, target_identifier: str, **kwargs
) -> None:
    """
    Creates an alert if a similar, unresolved alert doesn't already exist.
    This prevents spamming the alerts table with duplicate notifications.
    """
    statement = select(Alert).where(
        Alert.hospital_id == hospital_id,
        Alert.alert_type == alert_type,
        cast(Alert.message, String).like(f"%{target_identifier}%"),
        Alert.resolved == False,  # noqa
    )
    existing_alert = db.exec(statement).first()

    if not existing_alert:
        alert = Alert(
            hospital_id=hospital_id,
            alert_type=alert_type,
            resolved=False,
            created_at=datetime.utcnow(),
            **kwargs,
        )
        db.add(alert)
        db.commit()


def check_inventory_alerts(db: Session, *, hospital: Hospital) -> None:
    """Checks for medicine stock below reorder level."""
    assert hospital.id is not None, "Hospital must have an ID."

    # --- 1. Check for medicines below static reorder level ---
    low_stock_med_statement = select(Inventory).where(
        Inventory.hospital_id == hospital.id,
        Inventory.quantity < Inventory.reorder_level,
    )
    low_stock_items = db.exec(low_stock_med_statement).all()

    for item in low_stock_items:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="low_inventory",
            severity="warning",
            message=f"Low stock for medicine ID {item.medicine_id}. Current: {item.quantity}, Reorder at: {item.reorder_level}.",
            target_identifier=f"medicine_id:{item.medicine_id}",
        )

    # --- 2. Check for expiring medicines (within 30 days) ---
    expiry_horizon = datetime.utcnow().date() + timedelta(
        days=MEDICINE_EXPIRY_WARNING_DAYS
    )
    expiring_statement = select(Inventory).where(
        Inventory.hospital_id == hospital.id,
        Inventory.expiry_date != None,  # noqa
        col(Inventory.expiry_date) <= expiry_horizon,
    )
    expiring_items = db.exec(expiring_statement).all()

    for item in expiring_items:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="expiring_inventory",
            severity="info",
            message=f"Medicine ID {item.medicine_id} is expiring on {item.expiry_date}. Quantity: {item.quantity}.",
            target_identifier=f"medicine_id:{item.medicine_id}",
        )

    # --- 3. Check for test kits below static threshold ---
    kit_statement = (
        select(LabKit)
        .join(Laboratory)
        .where(Laboratory.hospital_id == hospital.id, LabKit.stock < LabKit.threshold)
    )
    low_stock_kits = db.exec(kit_statement).all()

    for kit in low_stock_kits:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="low_kit_inventory",
            severity="warning",
            message=f"Low stock for test kit '{kit.test_name}'. Current: {kit.stock}, Threshold: {kit.threshold}.",
            target_identifier=f"test_name:{kit.test_name}",
        )

    # --- 4. Check for medicines below forecasted demand ---
    # Find all inventory items that have a recent forecast.
    inventory_with_forecasts = db.exec(
        select(Inventory, Forecast)
        .join(
            Forecast,
            (col(Inventory.hospital_id) == col(Forecast.hospital_id))
            & (
                col(Forecast.target)
                == func.concat("medicine_id:", cast(Inventory.medicine_id, String))
            ),
        )
        .where(
            Inventory.hospital_id == hospital.id,
            Forecast.forecast_type == "medicine_demand",
            # Check if current quantity is less than the predicted demand for the next 7 days
            Inventory.quantity < Forecast.predicted_value,
        )
    ).all()

    for inventory, forecast in inventory_with_forecasts:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="forecasted_shortage",
            severity="critical",
            message=f"Forecasted shortage for medicine ID {inventory.medicine_id}. Current stock: {inventory.quantity}, but predicted demand is {forecast.predicted_value:.0f} for the next 7 days.",
            target_identifier=f"medicine_id:{inventory.medicine_id}",
        )

    # --- 5. Check for test kits below forecasted demand ---
    kit_with_forecasts = db.exec(
        select(LabKit, Forecast)
        .join(Laboratory, col(LabKit.laboratory_id) == col(Laboratory.id))
        .join(
            Forecast,
            (col(Laboratory.hospital_id) == col(Forecast.hospital_id))
            & (
                col(Forecast.target) == func.concat("test_name:", col(LabKit.test_name))
            ),
        )
        .where(
            Laboratory.hospital_id == hospital.id,
            Forecast.forecast_type == "kit_demand",
            # Check if current stock is less than the predicted demand for the next 7 days
            LabKit.stock < Forecast.predicted_value,
        )
    ).all()

    for kit, forecast in kit_with_forecasts:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="forecasted_kit_shortage",
            severity="critical",
            message=f"Forecasted shortage for test kit '{kit.test_name}'. Current stock: {kit.stock}, but predicted demand is {forecast.predicted_value:.0f} for the next 7 days.",
            target_identifier=f"test_name:{kit.test_name}",
        )


def check_bed_occupancy_alerts(db: Session, *, hospital: Hospital) -> None:
    """Checks if bed occupancy exceeds a critical threshold."""
    assert hospital.id is not None, "Hospital must have an ID."

    if hospital.total_beds > 0:
        # --- 1. Check current occupancy ---
        occupied_beds_count = db.exec(
            select(func.count(col(Bed.id))).where(
                Bed.hospital_id == hospital.id,
                Bed.occupied == True,  # noqa
            )
        ).one()
        occupancy_ratio = occupied_beds_count / hospital.total_beds
        if occupancy_ratio > BED_OCCUPANCY_CRITICAL_THRESHOLD:
            _create_alert_if_not_exists(
                db,
                hospital_id=hospital.id,
                alert_type="high_bed_occupancy",
                severity="critical",
                message=f"Bed occupancy is at {occupancy_ratio:.0%}, exceeding the {BED_OCCUPANCY_CRITICAL_THRESHOLD:.0%} threshold.",
                target_identifier=f"hospital_id:{hospital.id}",
            )

        # --- 2. Check forecasted occupancy ---
        forecast_statement = select(Forecast).where(
            Forecast.hospital_id == hospital.id,
            Forecast.forecast_type == "bed_occupancy",
        )
        bed_forecast = db.exec(forecast_statement).first()

        if bed_forecast:
            forecasted_ratio = bed_forecast.predicted_value / hospital.total_beds
            if forecasted_ratio > FORECASTED_BED_OCCUPANCY_THRESHOLD:
                _create_alert_if_not_exists(
                    db,
                    hospital_id=hospital.id,
                    alert_type="forecasted_high_occupancy",
                    severity="warning",
                    message=f"High bed occupancy of {forecasted_ratio:.0%} is forecasted for {bed_forecast.forecast_for}. Predicted: {bed_forecast.predicted_value:.0f} beds.",
                    target_identifier=f"hospital_id:{hospital.id}",
                )


def check_disease_outbreak_alerts(
    db: Session, *, hospital: Hospital, disease_id: int
) -> None:
    """Checks for a spike in cases for a specific disease."""
    assert hospital.id is not None, "Hospital must have an ID."

    # Check cases today vs. average of the last 7 days
    today = datetime.utcnow().date()
    seven_days_ago = today - timedelta(days=7)

    # Cases today
    today_statement = select(Patient).where(
        Patient.hospital_id == hospital.id,
        Patient.disease_id == disease_id,
        Patient.registered_at >= today,
    )
    cases_today = len(db.exec(today_statement).all())

    # Average cases over the last week (excluding today)
    past_week_statement = select(Patient).where(
        Patient.hospital_id == hospital.id,
        Patient.disease_id == disease_id,
        Patient.registered_at >= seven_days_ago,
        Patient.registered_at < today,
    )
    cases_last_week = len(db.exec(past_week_statement).all())
    avg_daily_cases_last_week = cases_last_week / 7.0

    # Avoid division by zero and prevent alerts for low numbers (e.g., 1 case vs 0)
    if cases_today > 5 and (
        avg_daily_cases_last_week == 0
        or (cases_today / avg_daily_cases_last_week) > DISEASE_SPIKE_FACTOR
    ):
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="disease_spike",
            severity="critical",
            message=f"Potential disease outbreak for disease ID {disease_id}. {cases_today} new cases today, compared to a recent average of {avg_daily_cases_last_week:.1f} cases/day.",
            target_identifier=f"disease_id:{disease_id}",
        )


def check_staffing_and_infra_alerts(db: Session, *, hospital: Hospital) -> None:
    """Checks for doctor shortages and infrastructure issues."""
    assert hospital.id is not None, "Hospital must have an ID."

    # --- 1. Check for doctor shortages based on attendance ---
    today = datetime.utcnow().date()
    # Find doctors who are marked as absent today
    absent_doctors_statement = (
        select(Doctor)
        .join(DoctorAttendance, col(Doctor.id) == col(DoctorAttendance.doctor_id))
        .where(
            Doctor.hospital_id == hospital.id,
            DoctorAttendance.date == today,
            DoctorAttendance.status == False,  # noqa
        )
    )
    absent_doctors = db.exec(absent_doctors_statement).all()

    for doctor in absent_doctors:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="doctor_shortage",
            severity="warning",
            message=f"Doctor shortage: Dr. {doctor.name} ({doctor.specialization}) is marked absent today.",
            target_identifier=f"doctor_id:{doctor.id}",
        )

    # --- 2. Check for unavailable laboratories ---
    unavailable_labs_statement = select(Laboratory).where(
        Laboratory.hospital_id == hospital.id,
        Laboratory.status != "Operational",
    )
    unavailable_labs = db.exec(unavailable_labs_statement).all()

    for lab in unavailable_labs:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="lab_unavailable",
            severity="critical",
            message=f"Laboratory '{lab.name}' is unavailable. Status: {lab.status}.",
            target_identifier=f"laboratory_id:{lab.id}",
        )

    # --- 3. Check for overdue lab equipment maintenance ---
    maintenance_horizon = today - timedelta(days=EQUIPMENT_SERVICE_INTERVAL_MONTHS * 30)
    overdue_equipment_statement = (
        select(LabEquipment)
        .join(Laboratory, col(Laboratory.id) == col(LabEquipment.laboratory_id))
        .where(
            Laboratory.hospital_id == hospital.id,
            LabEquipment.last_service != None,  # noqa
            col(LabEquipment.last_service) <= maintenance_horizon,
        )
    )
    overdue_equipment = db.exec(overdue_equipment_statement).all()

    for equipment in overdue_equipment:
        _create_alert_if_not_exists(
            db,
            hospital_id=hospital.id,
            alert_type="maintenance_overdue",
            severity="warning",
            message=f"Maintenance overdue for '{equipment.equipment_name}' in lab ID {equipment.laboratory_id}. Last serviced on {equipment.last_service}.",
            target_identifier=f"equipment_id:{equipment.id}",
        )


def run_alert_engine_for_hospital(db: Session, *, hospital_id: int) -> None:
    """
    Runs all alert checks for a given hospital.
    This function can be triggered as a background task.
    """
    hospital = db.get(Hospital, hospital_id)
    if not hospital:
        return

    check_inventory_alerts(db, hospital=hospital)
    check_bed_occupancy_alerts(db, hospital=hospital)
    check_staffing_and_infra_alerts(db, hospital=hospital)

    # Example: You might run disease checks for a list of common seasonal diseases
    # For now, we'll imagine it's triggered for a specific disease.
    # check_disease_outbreak_alerts(db, hospital=hospital, disease_id=1) # Example disease_id
