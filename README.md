# SmartDoor

Facial Recognition Door Unlocking System

We built a software using OpenCV that, once trained with sufficient images, can recognize the people that live in a house and unlock the door for them! We built most of the facial recognition portion of this project at Boston Hacks. For the EC441 project, we implemented all the networking components to finalize the program.

Networking Components

We installed our facial recog program onto a raspberry pi, which will be attached to the door with a camera. However, training on many images takes a lot of computing power, which overheats the raspberry pi. To fix this issue, we set up a server that will handle the heavy load of training and constantly communicate and exchange data with the pi via UDP/TCP.
