from email.policy import default
from sqlalchemy import Boolean, Column, String, DateTime, BIGINT, Text
from .medidb import Base

class MediPatients(Base):
    __tablename__ = "patients"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    patient_name = Column(String(255), unique=True)
    age = Column(BIGINT)
    medication = Column(String(255))
    times_taken_per_day = Column(BIGINT)
    
class MediMedications(Base):
    __tablename__ = "patient_medications"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    patient_name = Column(String(255))
    medication = Column(String(255))
    times_taken_per_day = Column(BIGINT)
    
class MediMedicationTimes(Base):
    __tablename__ = "medication_times"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    patient_name = Column(String(255))
    medication = Column(String(255))
    dosage_amount = Column(String(255))
    medication_time = Column(DateTime, nullable=True)
    
class MediPatientMedicationHistory(Base):
    __tablename__ = "patient_medication_history"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    patient_name = Column(String(255))
    medication = Column(String(255))
    dosage_amount = Column(String(255))
    time_given = Column(DateTime, nullable=True)
    time_category = Column(String(255))
    given_by = Column(String(255))
    target_time = Column(String(255))
    
class MediTrackerStatus(Base):
    __tablename__ = "medi_tracker"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    status = Column(String(255))