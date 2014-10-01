host:=0.0.0.0
port:=9000
activate_venv=source venv/bin/activate
 
debug:
	$(activate_venv) && ./manage.py runserver $(host):$(port)
 
start-uwsgi:
	$(activate_venv) \
	&& uwsgi --socket 127.0.0.1:$(port) \
          --chdir $(shell pwd) \
          --wsgi-file base/wsgi.py \
          --master \
          --process 4 \
          --daemonize $(shell pwd)/logs/uwsgi.log \
          --pidfile $(shell pwd)/uwsgi.pid  
 
stop-uwsgi:
	$(activate_venv) && uwsgi --stop uwsgi.pid
 
reload-uwsgi: 
	$(activate_venv) && uwsgi --reload uwsgi.pid
 
collectstatic:
	$(activate_venv) \
	&& ./manage.py collectstatic --noinput
 
database:=malatang
password:=
db:
	-mysql -u root --password=$(password) -e \
		"drop database $(database)"
	mysql -u root --password=$(password) -e \
		"create database $(database)"
	$(activate_venv) && ./manage.py syncdb --noinput
 
venv:
	virtualenv venv --python=python2.7
	
deps:
	$(activate_venv) && pip install -r requirements.txt
	-npm install
	-bower install
	
.PHONY: debug \
	db \
	deps \
	venv \
	collectstatic \
	reload-uwsgi \
	start-uwsgi \
	stop-uwsgi

