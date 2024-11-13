#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/src/DynamixelSDK/ros/dynamixel_sdk"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/install/lib/python3/dist-packages:/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build" \
    "/usr/bin/python3" \
    "/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/src/DynamixelSDK/ros/dynamixel_sdk/setup.py" \
     \
    build --build-base "/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/build/DynamixelSDK/ros/dynamixel_sdk" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/install" --install-scripts="/home/yh/EE346_Mobile_Robot_Navigation_and_Control/turtlebot3_source_code/install/bin"
