# Robotaxi example 

## Introduction 

An Robotaxi example to drive in CARLA town with built in behavior. 

This can be observed from CARLA server window. 

CARLA behavior will be in charge of:

- global route planner
- behavior 
- local planner 
- pid controller 

## Code

[robotaxi](./proj/robotaxi.py)

## Usage

Start CARLA server

`./CarlaUE4.sh -prefernvidia`

Run robotaxi example script 

`python robotaxi.py` 

Generate other traffic vehicles and pedestrians in CARLA PythonAPI/examples

`python generate_traffic.py` 

Run carlaviz

`docker run -it --network="host" -e CARLAVIZ_HOST_IP=localhost -e CARLA_SERVER_IP=localhost -e CARLA_SERVER_PORT=2000 mjxu96/carlaviz:0.9.13`

## Reference

- [【仿真】 Carla之全局规划follow [4]](https://blog.csdn.net/qq_39537898/article/details/117563006)

## Performance

![Robotaxi without others vehicles](./img/robotaxi_wo.gif)

![robotaxi with other vehicles](./img/robotaxi_with.gif)

![robotaxi with other vehicles in carlaviz](./img/robotaxi_with_carlaviz.gif)