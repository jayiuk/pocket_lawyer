import pandas as pd
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SRC = os.getenv("DATA_SRC")
DST = os.getenv("SUM_DATA_DST")

def get_sum_data():
    """요약모델 튜닝용 데이터 획득"""
    
    