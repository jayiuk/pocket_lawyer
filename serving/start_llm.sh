#!/usr/bin/env bash
set -euo pipefail

# 실행 설정
MODEL="google/gemma-4-E4B-it"
HOST="0.0.0.0"
PORT=8007

GPU_IDS="0"
TP_SIZE=1
MAX_MODEL_LEN=8192
GPU_MEMORY_UTILIZATION=0.90

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/llm_logs"
LOG_FILE="${LOG_DIR}/llm_${PORT}.log"
PID_FILE="${LOG_DIR}/llm_${PORT}.pid"

mkdir -p "$LOG_DIR"

source "$HOME/anaconda3/etc/profile.d/conda.sh"
conda activate llm_server

# 기존 실행 여부 확인
if [[ -f "$PID_FILE" ]]; then
    OLD_PID="$(cat "$PID_FILE")"
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "기존 프로세스가 실행 중입니다. PID: ${OLD_PID}"
        exit 1
    fi
fi

export CUDA_VISIBLE_DEVICES="$GPU_IDS"



nohup vllm serve "$MODEL" \
    --host "$HOST" \
    --port "$PORT" \
    --tensor-parallel-size "$TP_SIZE" \
    --max-model-len "$MAX_MODEL_LEN" \
    --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION" \
    >> "$LOG_FILE" 2>&1 < /dev/null &

PID=$!
echo "$PID" > "$PID_FILE"

echo "vLLM 실행 요청 완료"
echo "PID: ${PID}"
echo "로그: ${LOG_FILE}"
