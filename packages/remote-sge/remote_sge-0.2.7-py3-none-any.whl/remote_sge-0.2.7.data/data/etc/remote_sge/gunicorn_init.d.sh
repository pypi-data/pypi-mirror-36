#! /bin/bash
### BEGIN INIT INFO
# Provides:          yourapp
# Required-Start:    nginx
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: The main django process
# Description:       The gunicorn process that receives HTTP requests
#                    from nginx
#
### END INIT INFO
#
# Author:       mle <geobi@makina-corpus.net>
#
USER=$$USER
PATH=/bin:/usr/bin:/sbin:/usr/sbin
GUNICORN=$$HOME/.pyenv/versions/remote_sge/bin/gunicorn
CONFIG_FILE=${dest_path}/gunicorn_config.py

case "$$1" in
  start)
        # log_daemon_msg "Starting deferred execution scheduler" "$$APPNAME"
        su -l $$USER -c "$$GUNICORN --daemon -m 007 -c $$CONFIG_FILE sge_server:app"
    ;;
  stop)
    killall gunicorn
    ;;
  restart)
    killall gunicorn
    su -l $$USER -c "$$GUNICORN --daemon -m 007 -c $$CONFIG_FILE sge_server:app"
    ;;
  status)
    ps aux | grep gunicorn
    ;;
  *)
    echo "Usage: /etc/init.d/$$APPNAME {start|stop|restart|force-reload|status}"
    exit 1
    ;;
esac

exit 0

