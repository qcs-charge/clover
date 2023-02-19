import api
import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
import time
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from mavros_msgs.srv import CommandBool


def navigate_wait(x: int, y: int, z: int, yaw=0, speed=0.5, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)
    k = 0
    while not rospy.is_shutdown() and k < 10:
        k += 1
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)


def land_to_qcs(x: float, y: float):
    navigate_wait(x=x, y=y, z=0.5, frame_id='aruco_map', tolerance=0.07)
    navigate_wait(x=x, y=y, z=0.3, frame_id='aruco_map', tolerance=0.05)
    navigate_wait(x=x, y=y, z=0.2, frame_id='aruco_map', tolerance=0.05)
    land()


rospy.init_node('flight')

arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

# flight
navigate_wait(x=0, y=0, z=0.4, frame_id='body', auto_arm=True)
navigate_wait(x=0, y=0, z=0.6, frame_id='aruco_15')
navigate_wait(x=0, y=0, z=0.6, frame_id='aruco_101')

# landing
land_to_qcs(x=0.95, y=0.95)
