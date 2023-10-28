import pandas as pd
from sqlalchemy import delete, select

import logging

from . import models 
from .medidb import engine

def create_tables(create: bool):
    '''
    Creates tables from models.py
    '''
    try:
        if create:
            models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error: {e}")
        
def read(query: str):
    '''
    Reads database using pandas with a supplied query and db engine
    '''
    try:
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        logging.error("commands.py - read: [{}]".format(e))
        
def insert(table: str, df: pd.DataFrame):
    '''
    Insert data into db table
    '''
    try:
        df.to_sql(table, engine, if_exists="append", index=False)
    except Exception as e:
        logging.error("commands.py - insert: [{}]".format(e))
        
def delete_patient_data(value):
    '''
    deletes row in database
    '''
    try:
        stmt_patients = delete(models.Base.metadata.tables[models.MediPatients.__tablename__]).where(models.MediPatients.patient_name == value)
        stmt_med_times = delete(models.Base.metadata.tables[models.MediMedicationTimes.__tablename__]).where(models.MediMedicationTimes.patient_name == value)
        stmt_med_history = delete(models.Base.metadata.tables[models.MediPatientMedicationHistory.__tablename__]).where(models.MediPatientMedicationHistory.patient_name == value)
        
        with engine.begin() as conn:
            conn.execute(stmt_patients)
            conn.execute(stmt_med_times)
            conn.execute(stmt_med_history)

    except Exception as e:
        logging.error("commands.py - delete_patient_row: [{}]".format(e))
        
def get_patient_data(patient_name: str):
    '''
    finds patient data from patients and medication_times tables based on patient_name
    '''
    try:
        stmt_patients = select(models.Base.metadata.tables[models.MediPatients.__tablename__]).where(models.MediPatients.patient_name == [patient_name])
        stmt_med_times = select(models.Base.metadata.tables[models.MediMedicationTimes.__tablename__]).where(models.MediMedicationTimes.patient_name == [patient_name])
    
        with engine.begin() as conn:
            patient = conn.execute(stmt_patients).first()
            med_times = conn.execute(stmt_med_times).all()
        
        return {"patient": patient, "med_times": med_times}

    except Exception as e:
        logging.error("commands.py - get_patient_data: [{}]".format(e))