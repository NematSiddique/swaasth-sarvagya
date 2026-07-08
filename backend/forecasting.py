import random
from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import func
from sqlmodel import Session, col, select

from app.models import (
    DailyBedStats,
    DailyInventoryUsage,
    Forecast,
    Hospital,
    Patient,
    PatientTest,
)

# In a real application, you would add 'prophet' to your dependencies
# and load your pre-trained model file.
#
# from prophet import Prophet
#
# # This model would be trained and saved by a separate offline process.
# model: Prophet = pd.read_pickle("path/to/your/prophet_model.pkl")

# --- Medicine Demand Forecasting ---


def generate_demand_forecast(
    db: Session, *, hospital: Hospital, medicine_id: int
) -> Forecast:
    """
    Generates a simulated medicine demand forecast for the next 7 days.

    This function simulates a real-world forecasting pipeline:
    1.  **Fetch Historical Data**: It queries the `DailyInventoryUsage` table.
        If no data exists, it generates a random historical dataset.
    2.  **Prepare Data**: It formats the data into a pandas DataFrame, as expected by models like Prophet.
    3.  **Simulate Model Prediction**: It simulates a call to a Prophet model's `predict` method.
    4.  **Save Forecast**: It stores the new forecast in the `Forecasts` table.
    """
    # 1. Fetch historical data (e.g., last 30 days)
    # The hospital object must have an ID to proceed.
    assert hospital.id is not None, "Hospital must have an ID to generate a forecast."

    # In a real scenario, you'd query your aggregated data table.
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    statement = select(DailyInventoryUsage).where(
        DailyInventoryUsage.hospital_id == hospital.id,
        DailyInventoryUsage.medicine_id == medicine_id,
        DailyInventoryUsage.date >= thirty_days_ago,
    )
    historical_data = db.exec(statement).all()

    # 2. Prepare data for the model (Prophet expects a DataFrame with 'ds' and 'y' columns)
    if not historical_data:
        # If no history, create a fake dataset for simulation purposes
        dates = pd.to_datetime(
            pd.date_range(end=datetime.utcnow(), periods=30, freq="D")
        )
        usage = [random.randint(5, 20) for _ in range(30)]
        history_df = pd.DataFrame({"ds": dates, "y": usage})
    else:
        history_df = pd.DataFrame(
            {
                "ds": [item.date for item in historical_data],
                "y": [item.used_today for item in historical_data],
            }
        )
        history_df["ds"] = pd.to_datetime(history_df["ds"])

    # 3. Simulate model prediction for the next 7 days
    # --- REAL IMPLEMENTATION ---
    # future_df = model.make_future_dataframe(periods=7)
    # forecast_df = model.predict(future_df)
    # predicted_demand = forecast_df.loc[forecast_df.index[-1], 'yhat']
    # confidence_upper = forecast_df.loc[forecast_df.index[-1], 'yhat_upper']
    # confidence_lower = forecast_df.loc[forecast_df.index[-1], 'yhat_lower']
    # confidence = 1 - ((confidence_upper - confidence_lower) / predicted_demand) if predicted_demand > 0 else 0.5

    # --- SIMULATED IMPLEMENTATION ---
    # We simulate the output of the real implementation above.
    avg_daily_usage = history_df["y"].mean()
    predicted_demand = avg_daily_usage * 7

    # Simulate confidence interval based on historical variance
    std_dev = history_df["y"].std()
    # A wider variance in past data leads to lower confidence
    confidence = max(0.5, 1 - (std_dev / avg_daily_usage if avg_daily_usage > 0 else 1))

    # 4. Create and save the new forecast object
    forecast_for_date = datetime.utcnow().date() + timedelta(days=7)

    # Check if a forecast for this target and date already exists
    statement = select(Forecast).where(
        Forecast.hospital_id == hospital.id,
        Forecast.target == f"medicine_id:{medicine_id}",
        Forecast.forecast_for == forecast_for_date,
    )
    existing_forecast = db.exec(statement).first()

    if existing_forecast:
        db_forecast = existing_forecast
        db_forecast.predicted_value = predicted_demand
        db_forecast.confidence = confidence
        db_forecast.generated_at = datetime.utcnow()
    else:
        db_forecast = Forecast(
            hospital_id=hospital.id,
            forecast_type="medicine_demand",
            target=f"medicine_id:{medicine_id}",
            predicted_value=predicted_demand,
            forecast_for=forecast_for_date,
            confidence=confidence,
            generated_at=datetime.utcnow(),
        )
        db.add(db_forecast)

    db.commit()
    db.refresh(db_forecast)
    return db_forecast


def trigger_medicine_forecast_update(
    db: Session, *, hospital_id: int, medicine_id: int
) -> None:
    """Triggers a background task to update medicine forecast."""
    hospital = db.get(Hospital, hospital_id)
    if hospital:
        generate_demand_forecast(db, hospital=hospital, medicine_id=medicine_id)


# --- Bed Occupancy Forecasting ---


def generate_bed_occupancy_forecast(db: Session, *, hospital: Hospital) -> Forecast:
    """
    Generates a simulated bed occupancy forecast for the next 7 days.
    """
    assert hospital.id is not None, "Hospital must have an ID to generate a forecast."

    # 1. Fetch historical data from DailyBedStats
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    statement = select(DailyBedStats).where(
        DailyBedStats.hospital_id == hospital.id,
        DailyBedStats.date >= thirty_days_ago,
    )
    historical_data = db.exec(statement).all()

    # 2. Prepare data for the model
    if not historical_data:
        # Simulate occupancy for the last 30 days if no history
        dates = pd.to_datetime(
            pd.date_range(end=datetime.utcnow(), periods=30, freq="D")
        )
        # Simulate occupancy as a percentage of total beds
        occupancy = [
            random.randint(
                int(hospital.total_beds * 0.6), int(hospital.total_beds * 0.9)
            )
            for _ in range(30)
        ]
        history_df = pd.DataFrame({"ds": dates, "y": occupancy})
    else:
        history_df = pd.DataFrame(
            {
                "ds": [item.date for item in historical_data],
                "y": [item.occupied for item in historical_data],
            }
        )
        history_df["ds"] = pd.to_datetime(history_df["ds"])

    # 3. Simulate model prediction for the next 7 days
    avg_daily_occupancy = history_df["y"].mean()
    # For occupancy, we predict the average for a future date, not a sum
    predicted_occupancy = avg_daily_occupancy

    std_dev = history_df["y"].std()
    confidence = max(
        0.5, 1 - (std_dev / avg_daily_occupancy if avg_daily_occupancy > 0 else 1)
    )

    # 4. Create and save the new forecast object
    forecast_for_date = datetime.utcnow().date() + timedelta(days=7)
    target = f"hospital_id:{hospital.id}"

    statement = select(Forecast).where(
        Forecast.hospital_id == hospital.id,
        Forecast.forecast_type == "bed_occupancy",
        Forecast.target == target,
        Forecast.forecast_for == forecast_for_date,
    )
    existing_forecast = db.exec(statement).first()

    if existing_forecast:
        db_forecast = existing_forecast
        db_forecast.predicted_value = predicted_occupancy
        db_forecast.confidence = confidence
        db_forecast.generated_at = datetime.utcnow()
    else:
        db_forecast = Forecast(
            hospital_id=hospital.id,
            forecast_type="bed_occupancy",
            target=target,
            predicted_value=predicted_occupancy,
            forecast_for=forecast_for_date,
            confidence=confidence,
            generated_at=datetime.utcnow(),
        )
        db.add(db_forecast)

    db.commit()
    db.refresh(db_forecast)
    return db_forecast


# --- Test Kit Demand Forecasting ---


def generate_kit_demand_forecast(
    db: Session, *, hospital: Hospital, test_name: str
) -> Forecast:
    """
    Generates a simulated test kit demand forecast for the next 7 days.
    """
    assert hospital.id is not None, "Hospital must have an ID to generate a forecast."

    # 1. Fetch historical data by aggregating PatientTest records
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    statement = (
        select(
            func.date(PatientTest.ordered_at).label("date"),
            func.count().label("usage"),
        )
        .join(
            Patient,
            col(Patient.id) == col(PatientTest.patient_id),
        )
        .where(
            Patient.hospital_id == hospital.id,
            PatientTest.test_name == test_name,
            func.date(PatientTest.ordered_at) >= thirty_days_ago,
        )
        .group_by(func.date(PatientTest.ordered_at))
        .order_by(func.date(PatientTest.ordered_at))
    )
    historical_data = db.exec(statement).all()

    # 2. Prepare data for the model
    if not historical_data:
        # Simulate usage for the last 30 days if no history
        dates = pd.to_datetime(
            pd.date_range(end=datetime.utcnow(), periods=30, freq="D")
        )
        usage = [random.randint(2, 15) for _ in range(30)]
        history_df = pd.DataFrame({"ds": dates, "y": usage})
    else:
        history_df = pd.DataFrame(
            {
                "ds": [item[0] for item in historical_data],
                "y": [item[1] for item in historical_data],
            }
        )
        history_df["ds"] = pd.to_datetime(history_df["ds"])

    # 3. Simulate model prediction for the next 7 days
    avg_daily_usage = history_df["y"].mean()
    predicted_demand = avg_daily_usage * 7

    std_dev = history_df["y"].std()
    confidence = max(0.5, 1 - (std_dev / avg_daily_usage if avg_daily_usage > 0 else 1))

    # 4. Create and save the new forecast object
    forecast_for_date = datetime.utcnow().date() + timedelta(days=7)
    target = f"test_name:{test_name}"

    statement = select(Forecast).where(
        Forecast.hospital_id == hospital.id,
        Forecast.forecast_type == "kit_demand",
        Forecast.target == target,
        Forecast.forecast_for == forecast_for_date,
    )
    existing_forecast = db.exec(statement).first()

    if existing_forecast:
        db_forecast = existing_forecast
        db_forecast.predicted_value = predicted_demand
        db_forecast.confidence = confidence
        db_forecast.generated_at = datetime.utcnow()
    else:
        db_forecast = Forecast(
            hospital_id=hospital.id,
            forecast_type="kit_demand",
            target=target,
            predicted_value=predicted_demand,
            forecast_for=forecast_for_date,
            confidence=confidence,
            generated_at=datetime.utcnow(),
        )
        db.add(db_forecast)

    db.commit()
    db.refresh(db_forecast)
    return db_forecast


# --- Disease Outbreak Forecasting ---


def generate_disease_outbreak_forecast(
    db: Session, *, hospital: Hospital, disease_id: int
) -> Forecast:
    """
    Generates a simulated forecast for new cases of a specific disease.
    """
    assert hospital.id is not None, "Hospital must have an ID to generate a forecast."

    # 1. Fetch historical data by aggregating Patient records
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    statement = (
        select(
            func.date(Patient.registered_at).label("date"),
            func.count().label("patient_count"),
        )
        .where(
            Patient.hospital_id == hospital.id,
            Patient.disease_id == disease_id,
            func.date(Patient.registered_at) >= thirty_days_ago,
        )
        .group_by(func.date(Patient.registered_at))
        .order_by(func.date(Patient.registered_at))
    )
    historical_data = db.exec(statement).all()

    # 2. Prepare data for the model
    if not historical_data:
        # Simulate new cases for the last 30 days if no history
        dates = pd.to_datetime(
            pd.date_range(end=datetime.utcnow(), periods=30, freq="D")
        )
        # Simulate a low base rate of new cases
        usage = [random.randint(0, 5) for _ in range(30)]
        history_df = pd.DataFrame({"ds": dates, "y": usage})
    else:
        history_df = pd.DataFrame(
            {
                "ds": [item[0] for item in historical_data],
                "y": [item[1] for item in historical_data],
            }
        )
        history_df["ds"] = pd.to_datetime(history_df["ds"])

    # 3. Simulate model prediction for the next 7 days
    avg_daily_cases = history_df["y"].mean()
    predicted_cases = avg_daily_cases * 7

    std_dev = history_df["y"].std()
    confidence = max(0.5, 1 - (std_dev / avg_daily_cases if avg_daily_cases > 0 else 1))

    # 4. Create and save the new forecast object
    forecast_for_date = datetime.utcnow().date() + timedelta(days=7)
    target = f"disease_id:{disease_id}"

    statement = select(Forecast).where(
        Forecast.hospital_id == hospital.id,
        Forecast.forecast_type == "disease_outbreak",
        Forecast.target == target,
        Forecast.forecast_for == forecast_for_date,
    )
    existing_forecast = db.exec(statement).first()

    if existing_forecast:
        db_forecast = existing_forecast
        db_forecast.predicted_value = predicted_cases
        db_forecast.confidence = confidence
        db_forecast.generated_at = datetime.utcnow()
    else:
        db_forecast = Forecast(
            hospital_id=hospital.id,
            forecast_type="disease_outbreak",
            target=target,
            predicted_value=predicted_cases,
            forecast_for=forecast_for_date,
            confidence=confidence,
            generated_at=datetime.utcnow(),
        )
        db.add(db_forecast)

    db.commit()
    db.refresh(db_forecast)
    return db_forecast
