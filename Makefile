include .env


.PHONY: dc-start
dc-start:
	@docker-compose stop;
	@docker-compose build;
	@docker-compose up -d;

.PHONY: dc-stop
dc-stop:
	@docker-compose stop;

.PHONY: dc-cleanup
dc-cleanup:
	@docker rm $(shell docker ps -qa --no-trunc --filter "status=exited");
	@docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc);

.PHONY: dc-reboot
dc-reboot:
	@docker-compose stop;
	printf 'y' | sudo docker system prune;
	@docker-compose build;
	@docker-compose up -d;

.PHONY: dc-start-local
dc-start-local:
	@docker-compose stop;
	@docker-compose build;
	@docker-compose up --scale nginx=0;

.PHONY: dc-ps
dc-ps:
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}";

.PHONY: dc-pg
dc-pg:
	@docker-compose up db;

.PHONY: dc-psql
dc-psql:
	@docker exec -it juniper_db_1 psql -U pguser pgdb
