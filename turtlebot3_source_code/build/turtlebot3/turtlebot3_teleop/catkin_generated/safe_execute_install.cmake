execute_process(COMMAND "/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/turtlebot3/turtlebot3_teleop/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/turtlebot3/turtlebot3_teleop/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
