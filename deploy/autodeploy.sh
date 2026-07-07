#!/bin/bash
# =========================================================
# mining 자동 배포 스크립트 (홈서버: /opt/lang/mining)
#
# 설치(최초 1회, 홈서버에서):
#   cd /opt/lang/mining && bash deploy/autodeploy.sh install
#
# 동작:
#   cron이 2분마다 실행
#   - 새 커밋 없음 -> 아무 것도 안 함
#   - HTML/문제JSON/데이터만 변경 -> pull만 (재시작 없음, 즉시 반영)
#   - server.js/package.json 변경 -> pull + npm install + 재시작
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
}

if [ "$1" = "install" ]; then
    chmod +x "$APP_DIR/deploy/autodeploy.sh"
    ( crontab -l 2>/dev/null | grep -v 'deploy/autodeploy.sh' ; \
      echo "*/2 * * * * $APP_DIR/deploy/autodeploy.sh >> $DEPLOY_LOG 2>&1" ) | crontab -
    echo "$(date '+%F %T') cron installed for $APP_DIR" >> "$DEPLOY_LOG"
    echo "[OK] cron 등록 완료: 2분마다 자동 배포 ($APP_DIR)"
    start_app
    echo "[OK] 앱 기동 완료 (port $PORT, pid $(cat "$PID_FILE"))"
    exit 0
fi

cd "$APP_DIR" || exit 1
OLD=$(git rev-parse HEAD)
git pull --ff-only >> "$DEPLOY_LOG" 2>&1
NEW=$(git rev-parse HEAD)

if [ "$OLD" != "$NEW" ]; then
    CHANGED=$(git diff --name-only "$OLD" "$NEW")
    echo "$(date '+%F %T') deploy $OLD -> $NEW" >> "$DEPLOY_LOG"
    if echo "$CHANGED" | grep -qE '^(server\.js|package.*\.json|requirements\.txt|deploy/)'; then
        npm install --omit=dev >> "$DEPLOY_LOG" 2>&1
        start_app
        echo "$(date '+%F %T') server files changed -> restarted" >> "$DEPLOY_LOG"
    else
        echo "$(date '+%F %T') content-only change -> no restart" >> "$DEPLOY_LOG"
    fi
fi

# 앱이 죽어 있으면 되살리기 (watchdog)
if ! app_running; then
    echo "$(date '+%F %T') app not running -> restart" >> "$DEPLOY_LOG"
    start_app
fi
