# step2
# path planning and visualize route 
# https://github.com/carla-simulator/carla/discussions/4528

# step1
# visualize generated spawn_points 
# https://carla.readthedocs.io/en/latest/tuto_G_getting_started/#using-and-visualizing-map-spawn-points

import carla
import numpy as np
from agents.navigation.global_route_planner import GlobalRoutePlanner

distance = 2.0

client = carla.Client('localhost',2000)
world = client.get_world()
m = world.get_map()
transform = carla.Transform()
spectator = world.get_spectator()
bv_transform = carla.Transform(transform.location + carla.Location(z=250,x=0), carla.Rotation(yaw=0, pitch=-90))
spectator.set_transform(bv_transform)

blueprint_library = world.get_blueprint_library()
spawn_points = m.get_spawn_points()

for i, spawn_point in enumerate(spawn_points):
    world.debug.draw_string(spawn_point.location, str(i), life_time=100)
    world.debug.draw_arrow(spawn_point.location, spawn_point.location + spawn_point.get_forward_vector(), life_time=100)


origin = carla.Location(spawn_points[98].location)
destination = carla.Location(spawn_points[75].location)        

grp = GlobalRoutePlanner(m, distance)
route = grp.trace_route(origin, destination)

T = 100
for pi, pj in zip(route[:-1], route[1:]):
    pi_location = pi[0].transform.location
    pj_location = pj[0].transform.location 
    pi_location.z = 0.5
    pj_location.z = 0.5
    world.debug.draw_line(pi_location, pj_location, thickness=0.2, life_time=T, color=carla.Color(r=255))
    pi_location.z = 0.6
    world.debug.draw_point(pi_location, color=carla.Color(r=255), life_time=T)   
    
while True:
    world.wait_for_tick()
