#!/bin/bash
# =========================================================
# mining 배포 스크립트 (홈서버: /opt/lang/mining) - 수동 배포 방식
#
# 사용법:
#   bash deploy/autodeploy.sh            # 배포: git pull + 필요 시에만 재시작
#   bash deploy/autodeploy.sh restart    # 강제 재시작 (최초 설정 직후 1회 사용)
#   bash deploy/autodeploy.sh install    # (선택) cron 자동배포 등록 - 현재 미사용
#
# 안전장치:
#   PID 파일(app.pid)로 mining 프로세스만 정확히 관리.
#   같은 서버의 다른 node 서비스(/opt/lang 등)는 절대 건드리지 않음.
#
# 로그: <APP_DIR>/deploy.log (배포) <APP_DIR>/app.log (앱)
# =========================================================

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${PORT:-9003}"          # 홈서버 서비스 포트
PID_FILE="$APP_DIR/app.pid"
DEPLOY_LOG="$APP_DIR/deploy.log"
APP_LOG="$APP_DIR/app.log"

app_running() {
    [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

stop_app() {
    if app_running; then
        kill "$(cat "$PID_FILE")" 2>/dev/null
        sleep 1
    fi
    rm -f "$PID_FILE"
}

start_app() {
    stop_app
    cd "$APP_DIR" || exit 1
    PORT="$PORT" nohup node server.js >> "$APP_LOG" 2>&1 &
    echo $! > "$PID_FILE"
    echo "$(date '+%F %T') app started on port $PORT (pid $(cat "$PID_FILE"))" >> "$DEPLOY_LOG"
    echo "[OK] 앱 기동 완료 (port $PORT, pid $(cat "$PID_FILE"))"
}

if [ "$1" = "restart" ]; then
    start_app
    exit 0
fi

if [ "$1" = "install" ]; then
    chmod +x "$APP_DIR/deploy/autodeploy.sh"
    ( crontab -l 2>/dev/null | grep -v 'deploy/autodeploy.sh' ; \
      echo "*/2 * * * * $APP_DIR/deploy/autodeploy.sh >> $DEPLOY_LOG 2>&1" ) | crontab -
    echo "[OK] cron 등록 완료: 2분마다 자동 배포 ($APP_DIR)"
    start_app
    exit 0
fi

# ===== 기본: 수동 배포 (pull + 필요 시에만 재시작) =====
cd "$APP_DIR" || exit 1
OLD=$(git rev-parse HEAD)
git pull --ff-only origin main 2>&1 | tee -a "$DEPLOY_LOG"
NEW=$(git rev-parse HEAD)

if [ "$OLD" = "$NEW" ]; then
    echo "[OK] 이미 최신 상태입니다 ($NEW)"
else
    CHANGED=$(git diff --name-only "$OLD" "$NEW")
    echo "$(date '+%F %T') deploy $OLD -> $NEW" >> "$DEPLOY_LOG"
    if echo "$CHANGED" | grep -qE '^(server\.js|package.*\.json|requirements\.txt|deploy/)'; then
        echo "[..] 서버 코드 변경 감지 -> 의존성 갱신 + 재시작"
        npm install --omit=dev >> "$DEPLOY_LOG" 2>&1
        start_app
    else
        echo "[OK] 콘텐츠만 변경 -> 재시작 없이 즉시 반영 완료"
    fi
fi

# 앱이 죽어 있으면 되살리기
if ! app_running; then
    echo "[..] 앱이 꺼져 있어 기동합니다"
    start_app
fi
