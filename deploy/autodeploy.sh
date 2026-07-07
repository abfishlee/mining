#!/bin/bash
# =========================================================
# mining 자동 배포 스크립트 (홈서버용)
#
# 설치(최초 1회, 홈서버에서):
#   cd /opt/lang && git pull && bash deploy/autodeploy.sh install
#
# 이후 동작:
#   cron이 2분마다 이 스크립트를 실행
#   -> GitHub에 새 커밋이 있으면 pull 후 앱 자동 재시작
#   -> 변경이 없으면 아무 것도 하지 않음
#
# 로그:
#   배포 로그: /tmp/mining_deploy.log
#   앱 로그  : /tmp/mining_app.log
# =========================================================

APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${PORT:-9002}"          # 홈서버 서비스 포트 (필요시 수정)
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
    # 기존 등록 제거 후 재등록 (중복 방지)
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
    echo "$(date '+%F %T') deploy $OLD -> $NEW" >> "$DEPLOY_LOG"
    npm install --omit=dev >> "$DEPLOY_LOG" 2>&1
    start_app
fi

# 앱이 죽어 있으면 되살리기 (watchdog)
if ! pgrep -f "node server.js" > /dev/null; then
    echo "$(date '+%F %T') app not running -> restart" >> "$DEPLOY_LOG"
    start_app
fi
