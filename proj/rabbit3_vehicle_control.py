# step3
# control vehicle to follow route with PID
# https://github.com/carla-simulator/carla/issues/3883
# https://github.com/Zhuweilong123/carla_learning/blob/master/design_a_route_for_ego-vehicle

# step2
# path planning and visualize route 
# https://github.com/carla-simulator/carla/discussions/4528

# step1
# visualize generated spawn_points 
# https://carla.readthedocs.io/en/latest/tuto_G_getting_started/#using-and-visualizing-map-spawn-points

import carla
import numpy as np
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.controller import VehiclePIDController
from agents.tools.misc import draw_waypoints, distance_vehicle, vector

distance = 2.0

client = carla.Client('localhost',2000)
world = client.get_world()
m = world.get_map()
transform = carla.Transform()
spectator = world.get_spectator()
bv_transform = carla.Transform(transform.location + carla.Location(z=200,x=0), carla.Rotation(yaw=0, pitch=-90))
spectator.set_transform(bv_transform)

blueprint_library = world.get_blueprint_library()
spawn_points = m.get_spawn_points()

for i, spawn_point in enumerate(spawn_points):
    world.debug.draw_string(spawn_point.location, str(i), life_time=100)
    world.debug.draw_arrow(spawn_point.location, spawn_point.location + spawn_point.get_forward_vector(), life_time=100)

# global path planner 
origin = carla.Location(spawn_points[98].location)
destination = carla.Location(spawn_points[27].location)        

grp = GlobalRoutePlanner(m, distance)
route = grp.trace_route(origin, destination)

wps = []
for i in range(len(route)):
    wps.append(route[i][0])
draw_waypoints(world, wps)

T = 100
for pi, pj in zip(route[:-1], route[1:]):
    pi_location = pi[0].transform.location
    pj_location = pj[0].transform.location 
    pi_location.z = 0.5
    pj_location.z = 0.5
    world.debug.draw_line(pi_location, pj_location, thickness=0.2, life_time=T, color=carla.Color(b=255))
    pi_location.z = 0.6
    world.debug.draw_point(pi_location, color=carla.Color(b=255), life_time=T)   
    
# spawn ego vehicle
ego_bp = blueprint_library.find('vehicle.tesla.cybertruck')
ego = world.spawn_actor(ego_bp, spawn_points[98])

# PID
#args_lateral_dict = {'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': 0.05}
args_lateral_dict = {'K_P': 1.95,'K_D': 0.2,'K_I': 0.07,'dt': 1.0 / 10.0}

#args_long_dict = {'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': 0.05}
args_long_dict = {'K_P': 1,'K_D': 0.0,'K_I': 0.75,'dt': 1.0 / 10.0}

PID=VehiclePIDController(ego,args_lateral=args_lateral_dict,args_longitudinal=args_long_dict)

i = 0
target_speed = 30
next = wps[0]
    
while True:
    
    ego_transform = ego.get_transform()
    spectator.set_transform(carla.Transform(ego_transform.location + carla.Location(z=80), carla.Rotation(pitch=-90)))
    
    ego_loc = ego.get_location()
    world.debug.draw_point(ego_loc, color=carla.Color(r=255), life_time=T)
    world.debug.draw_point(next.transform.location, color=carla.Color(r=255), life_time=T)      
    ego_dist = distance_vehicle(next, ego_transform)
    ego_vect = vector(ego_loc, next.transform.location)
    control = PID.run_step(target_speed, next)
    
    if i == (len(wps)-1):
        control = PID.run_step(0, wps[-1])
        ego.apply_control(control)
        print('this trip finish')
        break
    
    if ego_dist < 1.5: 
        i = i + 1
        next = wps[i]
        control = PID.run_step(target_speed, next)

    ego.apply_control(control)
    world.wait_for_tick()
