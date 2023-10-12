# -*- coding: utf-8 -*-
from typing import Optional

import requests

# Copyright 2021 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


'''
    The RobotAPI class is a wrapper for API calls to the robot. Here users
    are expected to fill up the implementations of functions which will be used
    by the RobotCommandHandle. For example, if your robot has a REST API, you
    will need to make http request calls to the appropriate endpoints within
    these functions.
'''


class RobotAPI:
    # The constructor below accepts parameters typically required to submit
    # http requests. Users should modify the constructor as per the
    # requirements of their robot's API
    def __init__(self, prefix: str, user: str, password: str) -> None:
        self.prefix = prefix
        self.user = user
        self.password = password
        self.connected = False
        # Test connectivity
        connected = self.check_connection()
        if connected:
            print("Successfully able to query API server")
            self.connected = True
        else:
            print("Unable to query API server")

    def check_connection(self) -> bool:
        ''' Return True if connection to the robot API server is successful'''
        url = self.prefix + "/health"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def position(self, robot_name: str) -> Optional[list]:
        ''' Return [x, y, theta] expressed in the robot's coordinate frame or
            None if any errors are encountered'''
        url = self.prefix + "/current_position"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Convert to [x, y, theta]
                req = response.json()
                return req["position"]
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def navigate(self, robot_name: str, pose: list, map_name: str) -> bool:
        ''' Request the robot to navigate to pose:[x,y,theta] where x, y and
            and theta are in the robot's coordinate convention. This function
            should return True if the robot has accepted the request,
            else False'''
        url = self.prefix + "/navigate"
        position = {"x": pose[0], "y": pose[1], "theta": pose[2]}
        print(pose)
        try:
            response = requests.post(url, json=position)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def start_process(self, robot_name: str, process: str, map_name: str) -> bool:
        ''' Request the robot to begin a process. This is specific to the robot
            and the use case. For example, load/unload a cart for Deliverybot
            or begin cleaning a zone for a cleaning robot.
            Return True if the robot has accepted the request, else False'''
        try:
            print("process_start")
            return True
        except Exception as e:
            print(e)
            return False

    def stop(self, robot_name: str) -> bool:
        ''' Command the robot to stop.
            Return True if robot has successfully stopped. Else False'''
        url = self.prefix + "/stop_nav"
        data = {"bool": True}
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def navigation_remaining_duration(self, robot_name: str) -> float:
        ''' Return the number of seconds remaining for the robot to reach its
            destination'''
        url = self.prefix + "/nav_remaining_duration"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                res = response.json()
                return res["duration"]
            else:
                return 0.0
        except Exception as e:
            print(e)
            return 0.0

    def navigation_completed(self, robot_name: str) -> bool:
        ''' Return True if the robot has successfully completed its previous
            navigation request. Else False.'''

        url = self.prefix + "/nav_stat"
        try:
            response = requests.get(url)
            print(response)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def process_completed(self, robot_name: str) -> bool:
        ''' Return True if the robot has successfully completed its previous
            process request. Else False.'''

        try:
            print("process_completed")
            return True
        except Exception as e:
            print(e)
            return False

    def battery_soc(self, robot_name: str) -> float:
        ''' Return the state of charge of the robot as a value between 0.0
            and 1.0. Else return None if any errors are encountered'''
        url = self.prefix + "/soc"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                res = response.json()
                return res["soc"]
            else:
                return 0.0
        except Exception as e:
            print(e)
            return 0.0
