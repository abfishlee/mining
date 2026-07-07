#!/bin/bash
# =========================================================
# mining 자동 배포 스크립트 (홈서버용)
#
# 설치(최초 1회, 홈서버에서):
#   cd /opt/lang && git pull && bash deploy/autodeploy.sh install
#
# 동작:
#   cron이 2분마다 실행
#   - 새 커밋 없음 -> 아무 것도 안 함
#   - HTML/문제JSON/데이터만 변경 -> pull만 (재시작 없음, 즉시 반영)
#   - server.js/package.json 변경 -> pull + npm install + 재시작
#   즉, 공부 중 서버가 끊기는 일은 서버 코드 배포 때만 발생
#
# 로그: /tmp/mining_deploy.log (배포) /tmp/mining_app.log (앱)
# =========================================================

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${PORT:-9003}"          # 홈서버 서비스 포트
DEPLOY_LOG=/tmp/mining_deploy.log
APP_LOG=/tmp/mining_app.log

start_app() {
    pkill -f "node server.js" 2>/dev/null
    sleep 1
    cd "$APP_DIR" || exit 1
    PORT="$PORT" nohup node server.js >> "$APP_LOG" 2>&1 &
    echo "$(date '+%F %T') app started on port $PORT (pid $!)" >> "$DEPLOY_LOG"
}

if [ "$1" = "install" ]; then
    chmod +x "$APP_DIR/deploy/autodeploy.sh"
    ( crontab -l 2>/dev/null | grep -v 'deploy/autodeploy.sh' ; \
      echo "*/2 * * * * $APP_DIR/deploy/autodeploy.sh >> $DEPLOY_LOG 2>&1" ) | crontab -
    echo "$(date '+%F %T') cron installed for $APP_DIR" >> "$DEPLOY_LOG"
    echo "[OK] cron 등록 완료: 2분마다 자동 배포"
    start_app
    echo "[OK] 앱 기동 완료 (port $PORT)"
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
        # 서버 코드 변경 -> 의존성 갱신 + 재시작 필요
        npm install --omit=dev >> "$DEPLOY_LOG" 2>&1
        start_app
        echo "$(date '+%F %T') server files changed -> restarted" >> "$DEPLOY_LOG"
    else
        # 콘텐츠(HTML/문제/데이터)만 변경 -> 재시작 불필요, 즉시 반영됨
        echo "$(date '+%F %T') content-only change -> no restart" >> "$DEPLOY_LOG"
    fi
fi

# 앱이 죽어 있으면 되살리기 (watchdog)
if ! pgrep -f "node server.js" > /dev/null; then
    echo "$(date '+%F %T') app not running -> restart" >> "$DEPLOY_LOG"
    start_app
fi
