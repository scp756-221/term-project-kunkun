# Makefile for standalone Music service (S2)
VER=v0.8
SERVER1=`docker inspect s2 --format '{{.NetworkSettings.IPAddress}}'`
PORT1=30001
SERVER2=`docker inspect s1 --format '{{.NetworkSettings.IPAddress}}'`
PORT2=30002
build-mcli:
	docker image build -f Dockerfile -t mcli:$(VER) .

#standalone
run-mcli-music:
	docker container run -it --rm --name mcli mcli:$(VER) python3 mcli.py $(SERVER1) $(PORT1) music

run-mcli-user:
	docker container run -it --rm --name mcli mcli:$(VER) python3 mcli.py $(SERVER2) $(PORT2) user

#AWS
run-mcli:
	docker container run -it --rm --name mcli mcli:$(VER) python3 mcli.py $(SERVER) $(PORT) $(SERVICE)