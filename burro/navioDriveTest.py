from drivers import NavioPWM
import time

throttle_driver = NavioPWM(5)
steering_driver = NavioPWM(3)

throttle_driver.update(-1)
time.sleep(2)
throttle_driver.update(-.5)
time.sleep(2)
throttle_driver.update(0)
time.sleep(2)
throttle_driver.update(.5)
time.sleep(2)
throttle_driver.update(1)
time.sleep(2)
throttle_driver.update(.5)
time.sleep(2)
throttle_driver.update(0)
time.sleep(2)
throttle_driver.update(-1)
time.sleep(2)
