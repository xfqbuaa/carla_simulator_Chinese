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
