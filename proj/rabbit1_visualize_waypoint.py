# step1
# visualize generated spawn_points 
# https://carla.readthedocs.io/en/latest/tuto_G_getting_started/#using-and-visualizing-map-spawn-points

import carla

client = carla.Client('localhost',2000)
world = client.get_world()
#world.set_weather(world.get_weather().ClearNight)
m = world.get_map()
transform = carla.Transform()
spectator = world.get_spectator()
# Town10
bv_transform = carla.Transform(transform.location + carla.Location(z=250,x=0), carla.Rotation(yaw=0, pitch=-90))
# Town03
#bv_transform = carla.Transform(transform.location + carla.Location(z=500,x=0), carla.Rotation(yaw=0, pitch=-90))
# Town04
#bv_transform = carla.Transform(transform.location + carla.Location(z=800,x=-75), carla.Rotation(yaw=0, pitch=-90))
# Town06
#bv_transform = carla.Transform(transform.location + carla.Location(z=900,x=150, y=0), carla.Rotation(yaw=0, pitch=-90))
spectator.set_transform(bv_transform)

blueprint_library = world.get_blueprint_library()
spawn_points = m.get_spawn_points()

for i, spawn_point in enumerate(spawn_points):
    world.debug.draw_string(spawn_point.location, str(i), life_time=100)
    world.debug.draw_arrow(spawn_point.location, spawn_point.location + spawn_point.get_forward_vector(), life_time=100)
    
    
while True:
    world.wait_for_tick()
