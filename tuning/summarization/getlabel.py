from dotenv import load_dotenv
import json
import os
from pathlib import Path
import logging
import pandas as pd

load_dotenv()
logger = logging.getLogger(__name__)

ROOT = Path(os.getenv("DATA_DST"))
LABEL_KEY = "class"

def get_labels(file_path : Path) -> str:
    parent = file_path.parent.name
    grand = file_path.parent.parent.parent.parent.name
    return f"{grand}_{parent}"

def add_label_json(json_path : Path):
    label = get_labels(json_path)
    try:
        with json_path.open("r", encoding = "utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"{json_path} 읽기 실패 : {e}")
        return
    
    if not isinstance(data, dict):
        print(f"{json_path}가 dict이 아님 type = {type(data)}")
    logger.info("파일 로드 완료")
    data[LABEL_KEY] = label
    
    try:
        with json_path.open("w", encoding = "utf-8") as w:
            json.dump(data, w, ensure_ascii=False, indent=2)
        logger.info(f"{json_path} -> {LABEL_KEY} = {label}")
    except Exception as e:
        print(f"{json_path} failed : {e}")

def add_label_csv(csv_path : Path):
    label = get_labels(csv_path)
    
    try:
        df = pd.read_csv(csv_path, encoding = "utf-8")
    except Exception as e:
        print(f"{csv_path} load failed : {e}")
    
    if df.empty:
        print("df is empty")
        return
    
    df[LABEL_KEY] = label
    try:
        df.to_csv(csv_path, index = False, encoding = "utf-8")
        logger.info("labeling done")
    except Exception as e:
        print(f"labeling failed {e}")


def labeling(root_dir : Path):
    for json_path in root_dir.rglob("*.json"):
        if json_path.parent.parent is None:
            print(f"{json_path} 상위 디렉토리 2개 미만")
            continue
        add_label_json(json_path)
    
    for csv_path in root_dir.rglob("*.csv"):
        if csv_path.parent.parent is None:
            print(f"{csv_path} 상위 디렉토리 2개 미만")
            continue
        add_label_csv(csv_path)
        
def labeling_to_summary():
    """요약 모델용 라벨링"""
        

if __name__ == "__main__":
    labeling(ROOT)