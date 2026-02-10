#source ros in terminal and start isaacsim with ros2 bridge enabled
source /opt/ros/jazzy/setup.sh
cd isaacsim
./isaac-sim.selector.sh

#start the simulation

#open another terminal and start z1_bridge
source /opt/ros/jazzy/setup.sh
cd z1_usd_project
python3 z1_bridge.py

#in another terminal give trajectory 
ros2 topic pub --once /joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: ['joint1','joint2','joint3','joint4','joint5','joint6'],
  points: [
    {positions: [0,0,0,0,0,0], time_from_start: {sec: 0}},
    {positions: [0.5,-0.3,0.8,0,0.5,0], time_from_start: {sec: 3}},
    {positions: [0,0,0,0,0,0], time_from_start: {sec: 6}}
  ]
}"


