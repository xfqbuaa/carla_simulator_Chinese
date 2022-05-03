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

from carla_painter import CarlaPainter


def main():
    actor_list = []
    try:

        # initialize onen painter
        painter = CarlaPainter('localhost', 8089)
              
        # Create client and send request to the carla server. 
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

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
        
        # let CarlaViz know this vehicle is the ego vehicle.
        ego_vehicle_bp.set_attribute('role_name','ego')
        # spawn the vehicle
        ego_vehicle = world.spawn_actor(ego_vehicle_bp, spawn_point)   
        actor_list.append(ego_vehicle)

        # --------------
        # Add a RGB camera sensor to ego vehicle. 
        # --------------
        
        cam_bp = None
        cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        cam_bp.set_attribute("image_size_x",str(640))
        cam_bp.set_attribute("image_size_y",str(480))
        cam_bp.set_attribute("fov",str(52))
        cam_location = carla.Location(2,0,1)
        cam_rotation = carla.Rotation(0,0,0)
        cam_transform = carla.Transform(cam_location,cam_rotation)
        ego_cam = world.spawn_actor(cam_bp,cam_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        #ego_cam.listen(lambda image: image.save_to_disk('~/tutorial/output/%.6d.jpg' % image.frame))
        actor_list.append(ego_cam)
        
        # --------------
        # Add GNSS sensor to ego vehicle. 
        # --------------
   
        gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
        gnss_location = carla.Location(0,0,0)
        gnss_rotation = carla.Rotation(0,0,0)
        gnss_transform = carla.Transform(gnss_location,gnss_rotation)
        gnss_bp.set_attribute("sensor_tick",str(3.0))
        ego_gnss = world.spawn_actor(gnss_bp,gnss_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        def gnss_callback(gnss):
            print("GNSS measure:\n"+str(gnss)+'\n')
        #ego_gnss.listen(lambda gnss: gnss_callback(gnss))
        actor_list.append(ego_gnss)
        
        # --------------
        # Add IMU sensor to ego vehicle. 
        # --------------
        
        imu_bp = world.get_blueprint_library().find('sensor.other.imu')
        imu_location = carla.Location(0,0,0)
        imu_rotation = carla.Rotation(0,0,0)
        imu_transform = carla.Transform(imu_location,imu_rotation)
        imu_bp.set_attribute("sensor_tick",str(3.0))
        ego_imu = world.spawn_actor(imu_bp,imu_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        def imu_callback(imu):
            print("IMU measure:\n"+str(imu)+'\n')
        #ego_imu.listen(lambda imu: imu_callback(imu))
        actor_list.append(ego_imu)
        
        # --------------
        # Add Lidar sensor to ego vehicle. 
        # --------------
        
        lidar = None
        blueprint_lidar = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        blueprint_lidar.set_attribute('range', '30')
        blueprint_lidar.set_attribute('rotation_frequency', '10')
        blueprint_lidar.set_attribute('channels', '32')
        blueprint_lidar.set_attribute('lower_fov', '-30')
        blueprint_lidar.set_attribute('upper_fov', '30')
        blueprint_lidar.set_attribute('points_per_second', '56000')
        transform_lidar = carla.Transform(carla.Location(x=0.0, z=5.0))
        lidar = world.spawn_actor(blueprint_lidar, transform_lidar, attach_to=ego_vehicle)
        #lidar.listen(lambda data: do_something(data))
        actor_list.append(lidar)

        # we need to tick the world once to let the client update the spawn position
        world.tick()
        
        # save vehicles' trajectories to draw in the frontend
        trajectories = [[]]

        # create the behavior agent
        agent = BehaviorAgent(ego_vehicle, behavior='normal')

        # to avoid the destination and start position same
        if spawn_points[0].location != ego_vehicle.get_location():
            destination = spawn_points[0]
        else:
            destination = spawn_points[1]

        # generate the route
        agent.set_destination(destination.location)

        while True:
            world.tick()
            
            ego_location = ego_vehicle.get_location()
            ego_velocity = ego_vehicle.get_velocity()
            
            trajectories[0].append([ego_location.x, ego_location.y, ego_location.z])

            # draw trajectories
            painter.draw_polylines(trajectories)
            
            velocity_str = "{:.2f}, ".format(ego_velocity.x) + "{:.2f}".format(ego_velocity.y) \
                    + ", {:.2f}".format(ego_velocity.z)
            painter.draw_texts([velocity_str],
                        [[ego_location.x, ego_location.y, ego_location.z + 10.0]], size=20)
            
            # top view
            #spectator = world.get_spectator()
            #transform = ego_vehicle.get_transform()
            #spectator.set_transform(carla.Transform(transform.location + carla.Location(z=30),
            #                                        carla.Rotation(pitch=-90)))

            speed_limit = ego_vehicle.get_speed_limit()
            agent.get_local_planner().set_speed(speed_limit)

            control = agent.run_step(debug=False)
            ego_vehicle.apply_control(control)
            
            if agent.done():
                print("Target reached, mission accomplished...")
                break

    finally:
        
        if settings is not None:
            world.apply_settings(settings)
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        print('destroying actors done')
        

if __name__ == '__main__':
    
    main()
    
