from sqlalchemy import Integer, Float, String, DateTime, Column
from databank_mlops.app.db.db import Base, engine
from databank_mlops.app.schemas.predict import PredictRequest, PredictResponse
from datetime import datetime


class PredictionData(Base):
    __tablename__ = "seg_model_orig"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    occupation: str = Column(String, nullable=True)
    age: float = Column(Float, nullable=True)
    annual_income: float = Column(Float, nullable=True)
    num_of_loan: float = Column(Float, nullable=True)
    num_of_delayed_payment: float = Column(Float, nullable=True)
    changed_credit_limit: float = Column(Float, nullable=True)
    outstanding_debt: float = Column(Float, nullable=True)
    amount_invested_monthly: float = Column(Float, nullable=True)
    monthly_balance: float = Column(Float, nullable=True)
    monthly_inhand_salary: float = Column(Float, nullable=True)
    num_bank_accounts: float = Column(Float, nullable=True)
    num_credut_card: float = Column(Float, nullable=True)
    interest_rate: float = Column(Float, nullable=True)
    delay_from_due_date: float = Column(Float, nullable=True)
    num_credit_inquiries: float = Column(Float, nullable=True)
    credit_utilization_ratio: float = Column(Float, nullable=True)
    total_emi_per_month: float = Column(Float, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    pd: float = Column(Float, nullable=True)

    @classmethod
    def from_pydantic(
        cls, predict_request: PredictRequest, predict_response: PredictResponse
    ):
        return cls(
            occupation=predict_request.OCCUPATION,
            age=predict_request.AGE,
            annual_income=predict_request.ANNUAL_INCOME,
            num_of_loan=predict_request.NUM_OF_LOAN,
            num_of_delayed_payment=predict_request.NUM_OF_DELAYED_PAYMENT,
            changed_credit_limit=predict_request.CHANGED_CREDIT_LIMIT,
            outstanding_debt=predict_request.OUTSTANDING_DEBT,
            amount_invested_monthly=predict_request.AMOUNT_INVESTED_MONTHLY,
            monthly_balance=predict_request.MONTHLY_BALANCE,
            monthly_inhand_salary=predict_request.MONTHLY_INHAND_SALARY,
            num_bank_accounts=predict_request.NUM_BANK_ACCOUNTS,
            num_credut_card=predict_request.NUM_CREDIT_CARD,
            interest_rate=predict_request.INTEREST_RATE,
            delay_from_due_date=predict_request.DELAY_FROM_DUE_DATE,
            num_credit_inquiries=predict_request.NUM_CREDIT_INQUIRIES,
            credit_utilization_ratio=predict_request.CREDIT_UTILIZATION_RATIO,
            total_emi_per_month=predict_request.TOTAL_EMI_PER_MONTH,
            pd=predict_response.prediction,
        )


class DriftFeatures(Base):
    __tablename__ = "drift_features"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    feature: str = Column(String, nullable=True)
    drift: int = Column(Integer, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)


class DriftTarget(Base):
    __tablename__ = "drift_target"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    drift: int = Column(Integer, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)


class ModelPerfomance(Base):
    __tablename__ = "model_performance"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    metric: str = Column(String, nullable=True)
    value: float = Column(Float, nullable=True)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)


# Crear la tabla en la base de datos
Base.metadata.create_all(engine)
