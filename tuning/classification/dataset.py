from datasets import load_dataset
import os
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

class DataSet():
    def __init__(self):
        self.root_path = Path(os.getenv("DATA_DST"))
        self.output = "class"
        self.input = "input"
    
    def _load_data_json(self):
        """데이터 로드용 메서드. 여러 디렉토리에 여러 파일로 나뉘어져 있어서 필요함"""