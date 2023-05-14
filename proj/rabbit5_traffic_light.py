# Rabbit5 traffic light 
# Step5: individual unit to try traffic light control 
# 5.1 get traffic light 
# 5.2 get traffic pole 
# 5.3 get traffic light state 
# 5.4 red stop vehicle 
# 5.5 green start vehicle
# https://carla.readthedocs.io/en/latest/core_actors/#traffic-signs-and-traffic-lights


import carla 
import time 
import numpy as np

from agents.navigation.controller import VehiclePIDController
from agents.tools.misc import draw_waypoints, distance_vehicle, vector

client = carla.Client('localhost',2000)
world = client.get_world()
blueprint_library = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

ego_bp = blueprint_library.find('vehicle.tesla.cybertruck')
ego = world.spawn_actor(ego_bp, spawn_points[40])

spectator = world.get_spectator()
transform = ego.get_transform()
ego_trans = carla.Transform(transform.location + carla.Location(y=8, z=5), transform.rotation)
spectator.set_transform(ego_trans)

# PID
#args_lateral_dict = {'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': 0.05}
args_lateral_dict = {'K_P': 1.95,'K_D': 0.2,'K_I': 0.07,'dt': 1.0 / 10.0}

#args_long_dict = {'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': 0.05}
args_long_dict = {'K_P': 1,'K_D': 0.0,'K_I': 0.75,'dt': 1.0 / 10.0}

PID=VehiclePIDController(ego,args_lateral=args_lateral_dict,args_longitudinal=args_long_dict)

stop_speed = 0
target_speed = 25
wps = [world.get_map().get_waypoint(spawn_points[40].location), world.get_map().get_waypoint(spawn_points[87].location), world.get_map().get_waypoint(spawn_points[132].location), world.get_map().get_waypoint(spawn_points[154].location)]
i = 1
next = wps[i]

try:
    while True:
        transform = ego.get_transform()
        ego_trans = carla.Transform(transform.location + carla.Location(y=8, z=5), transform.rotation)
        spectator.set_transform(ego_trans)
    
        #Get the traffic light affecting a vehicle
        ego_loc = ego.get_location()
        ego_transform = ego.get_transform()
        control = PID.run_step(target_speed, next)
        ego_dist = distance_vehicle(next, ego_transform)
        traffic_light = ego.get_traffic_light()
        
        if i == (len(wps)-1):
            control = PID.run_step(0, wps[-1])
            ego.apply_control(control)
            print('this trip finish')
            break
    
        if ego_dist < 1.5: 
            i = i + 1
            next = wps[i]
            control = PID.run_step(target_speed, next)
        
        if ego.is_at_traffic_light():
            print(ego.get_traffic_light_state())
            
            #aff_wps = traffic_light.get_affected_lane_waypoints()
            #stop_wps = traffic_light.get_stop_waypoints()
            #for j in range(len(aff_wps)):
            #    world.debug.draw_point(aff_wps[j].transform.location, color=carla.Color(r=255), life_time=100)
            #world.debug.draw_point(aff_wps[3].transform.location, color=carla.Color(r=255), life_time=100)
            #for j in range(len(stop_wps)):
            #    world.debug.draw_point(stop_wps[j].transform.location, color=carla.Color(b=255), life_time=100)
             
            if ego.get_traffic_light_state() == carla.TrafficLightState.Red or ego.get_traffic_light_state() == carla.TrafficLightState.Yellow:
                print("Red/Yellow")
                control.throttle = 0.0
                control.brake = 0.5
                control.hand_brake = False
        
        ego.apply_control(control)
        world.wait_for_tick()
        
finally:
    time.sleep(50)
    ego.destroy()
