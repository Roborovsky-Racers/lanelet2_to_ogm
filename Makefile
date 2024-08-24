all:
	@docker compose up
	@sudo chown -R $(USER):$(USER) ./app/map/*

download:
	@wget https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-2024/main/aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/map/lanelet2_map.osm
	@mv lanelet2_map.osm ./app/map/

clean:
	@rm -rf ./app/map/occupancy_grid_map.pgm ./app/map/occupancy_grid_map.yaml