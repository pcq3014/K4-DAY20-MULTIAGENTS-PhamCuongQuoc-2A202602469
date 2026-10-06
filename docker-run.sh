#!/bin/sh
# Chạy một lệnh của lab trong Docker, với shell của tác tử bị cô lập:
#   - repo được mount ở /root/lab (/root có quyền 700), runner chạy bằng root;
#   - lệnh shell của tác tử chạy bằng user `nobody` (LAB_AGENT_USER) -> không đọc được bộ chấm,
#     tác vụ đánh giá hay kết quả cũ; chỉ thấy sandbox của chính nó.
# Build một lần:  docker build -t lab-deepagents .
# Ví dụ:          sh docker-run.sh python -m lab.runner --condition baseline --tasks learn
cd "$(dirname "$0")"
HERE="$(pwd -W 2>/dev/null || pwd)"     # pwd -W: đường dẫn Windows khi chạy từ Git bash
MSYS_NO_PATHCONV=1 exec docker run --rm --env-file .env \
  -e LAB_AGENT_USER=nobody -e PYTHONPATH=/root/lab/src -e PYTHONUNBUFFERED=1 \
  -v "$HERE:/root/lab" -w /root/lab lab-deepagents "$@"
