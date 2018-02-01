# Carla tutorial
## Run python client and server
* run the server in carla server mode

`./CarlaUE4.sh /Game/Maps/Town01 -carla-server -benchmark -fps=15 -windowed -ResX=800 -ResY=600`
* run the python client:

`./client_example.py -a`

## Error import carla server pb2
during run `./client_example.py`, there is a error showing below.

`RuntimeError: cannot import "carla_server_pb2.py", run the protobuf compiler to generate this file`

The main reason is Carla documents conflicts with anaconda environment.

You can not follow Carla document using `pip3` instead `pip` to install required software since the anaconda environment is already python3.

## What does autopilot means?
[github issues](https://github.com/carla-simulator/carla/issues/36)

autopilot we refer to the hard-coded AI inside the game, this AI takes advantage of all the privileged information available in game and has nothing to do with the learning approaches mention in the paper and video.

The AI control is sent every frame together with the measurements, you can send it back to the server to enable the autopilot, or modify if wanted to add for instance some noise to it. The gist that @lucosanta provided is a good example.

After 0.7.0 this is done with

```
measurements, sensor_data = carla_client.read_data()
control = measurements.player_measurements.autopilot_control
carla_client.send_control(control)
```

## Error 'pyconfig.h' file not found
during `./Setup.sh`, there is a error showing below.
```
./boost/python/detail/wrap_python.hpp:50:11: fatal error: 'pyconfig.h' file not found
# include <pyconfig.h>
          ^
1 error generated.

...failed updating 68 targets...
...skipped 12 targets...
...updated 95 targets...
```

* please make sure python-dev package is installed

`apt-get install python-dev`
* find pyconfig.h location

`locate pyconfig.h`

* In anaconda python 3.6 environment, export path

`export CPLUS_INCLUDE_PATH=/home/xufq/miniconda3/pkgs/python-3.6.0-0/include/python3.6m/
`
 * `./Setup.sh`

## Multi camera setting

[Multi-camera setting](https://github.com/carla-simulator/carla/issues/42)

## How to run run_CIL.py

* imitation learning should be running in python 2 environment.

Suggest using anaconda to setup python 2 environment and install all necessary library.  

`pip install future` if there are `ImportError: No module named builtins`

* In carla repository to get benchmark_branch

`git -b benchmark_branch origin/benchmark_branch`

then copy whole folder carla to imitation learning folder
`cp -r ./PythonClient/carla  ../imitation_learning`

Pay more attention to folder structure here.

* modify client.py

line 20: #from carla_protocol import EpisodeReady

line 100: pb_message = carla_protocol.EpisodeReady()

[reference](https://github.com/carla-simulator/carla/commit/30c54019ec84d533d0d3d5082b277c2c93040cbb)

* start server and run run_CIL.py in python 2 enviroment

##  Basic Carla design
[basic Carla design](https://github.com/carla-simulator/carla/issues/140)

"ASceneCaptureToDiskCamera"

"AVehicleSpawnerBase"

## Get information about npc vehicle's speed
[github send all vehicle information](https://github.com/carla-simulator/carla/issues/155)

## Separate segment for traffic lights and traffic Signs
[different segment for traffic lights and signs ](https://github.com/carla-simulator/carla/issues/175)

## Document guide
[document guide](https://github.com/carla-simulator/carla/issues/142)

## Navigation
[Navigation](https://github.com/carla-simulator/carla/issues/94)

We implemented our own controller, the code can be found at "WheeledVehicleAIController.cpp". We use information about the road lanes that is generated when building the map, as well as trigger volumes for traffic lights and signs.

The intersections are handled by IntersectionEntrance, otherwise the car just go straight until it finds a road patch with defined direction.

New RoutePlanner class for assigning fixed routes to autopilot (IntersectionEntrance has been removed)
