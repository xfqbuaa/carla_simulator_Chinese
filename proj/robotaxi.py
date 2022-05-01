# This script is to simulate a virtual robotaxi in the city and observe from Carla server window. 
# Version 0.1
# @Frank Xu
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>. 

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time  

# Import BehaviorAgent, which will be in charge of: 
# global route planner
# behavior 
# local planner
# controller pid    
from agents.navigation.behavior_agent import BehaviorAgent  # pylint: disable=import-error


def main():
    actor_list = []
    try:
        # Create client and send request to the carla server. 
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        # Retrieve the world that is currently running
        world = client.get_world()
        # Change Town map 
        #world = client.load_world('Town01')

        # set sync mode
        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()

        # read all valid spawn points
        # define ego vehicle init position 
        spawn_points = world.get_map().get_spawn_points()
        random.shuffle(spawn_points)
        # randomly choose one as the start point
        spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()

        # create the blueprint library
        ego_vehicle_bp = blueprint_library.find('vehicle.lincoln.mkz_2017')
        #ego_vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
        #ego_vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
        # spawn the vehicle
        vehicle = world.spawn_actor(ego_vehicle_bp, spawn_point)
        actor_list.append(vehicle)

        # we need to tick the world once to let the client update the spawn position
        world.tick()

        # create the behavior agent
        agent = BehaviorAgent(vehicle, behavior='normal')

        # to avoid the destination and start position same
        if spawn_points[0].location != vehicle.get_location():
            destination = spawn_points[0]
        else:
            destination = spawn_points[1]

        # generate the route
        agent.set_destination(destination.location)

        while True:
            world.tick()
            
            # top view
            spectator = world.get_spectator()
            transform = vehicle.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(z=30),
                                                    carla.Rotation(pitch=-90)))

            speed_limit = vehicle.get_speed_limit()
            agent.get_local_planner().set_speed(speed_limit)

            control = agent.run_step(debug=True)
            vehicle.apply_control(control)
            
            if agent.done():
                print("Target reached, mission accomplished...")
                break

    finally:
    
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        print('destroying actors done')
        

if __name__ == '__main__':
    
    main()
    
