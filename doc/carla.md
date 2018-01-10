# Carla tutorial
## Run python client and server
* run the server in carla server mode

`./CarlaUE4.sh /Game/Maps/Town01 -carla-server -benchmark -fps=15 -windowed -ResX=800 -ResY=600`
* run the python client:

`./client_example.py`
## Error import carla server pb2
during run `./client_example.py`, there is a error showing below.

`RuntimeError: cannot import "carla_server_pb2.py", run the protobuf compiler to generate this file`

The main reason is Carla documents conflicts with anaconda environment. You can not follow Carla document using `pip3` instead `pip` to install required software since the anaconda environment is already python3. 
