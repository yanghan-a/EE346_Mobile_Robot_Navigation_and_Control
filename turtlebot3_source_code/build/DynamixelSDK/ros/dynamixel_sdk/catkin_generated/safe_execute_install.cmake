execute_process(COMMAND "/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/DynamixelSDK/ros/dynamixel_sdk/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/DynamixelSDK/ros/dynamixel_sdk/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
