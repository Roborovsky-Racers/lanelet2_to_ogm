# lanelet2_to_ogm

## about
parse lanelet2(.osm) to occupancy grid map format(.pgm and .yaml)

## requirements
- docker
- docker compose
- make

## setup
```
wget https://raw.githubusercontent.com/AutomotiveAIChallenge/aichallenge-2024/main/aichallenge/workspace/src/aichallenge_submit/aichallenge_submit_launch/map/lanelet2_map.osm
mv lanelet2_map.osm ./app/map/
```

OR

```
make download
```

## parse lanelet2 to occupancy grid map
```
make
```
ogm generated to lanelet2_to_ogm/app/map/occupancy_grid_map.pgm and .yaml