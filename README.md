# Main: Full Scale Payload 2023: ARCHIE 

## The home of UMass Rocket Team's payload control software. For deployment on ARCHIE payload system

## Table of Contents
* About
* Hardware Specifications
* Branches
* Roadmap
* Acknowledgements
* License


# About

This repository houses all code used for the 2023 full-scale payload system. It is currently under development as the team approaches its launch deadlines.

# Hardware Specifications

* Main flight computer: Raspberry Pi 4B
* Secondary flight comupter: Raspberry Pi Pico

# Branches

* [image_processing](image_processing): Contains all image processing and horizon detection source code
* [pico_main](pico_main): Contains all communication source code for pico to BNO055, SD card, and Raspberry Pi 4
* [greenway](greenway): Contains all code contributed by Calista Greenway. This includes comms for pico, servo rotation, xbee comms, and camera init source code.
* [liousas](liousas): Contains all code contributed by Demetri Liousas. Includes launch-landing detection, flight time calculation, and simulation data.
* [motor_control](motor_control): Contains all motor control source code, for general motor control (non-specified)

# Acknowledgements

Payload Subteam:

* Calista Greenway (goobway): Payload Lead and Contributor
* Demetri Liousas (dliousas): Contributor
* Mitchell Sylvia (belgianlion): Contributor
* Junyang Lu (Jun-L04): Contributor
* Anton Voronov (ravenspired): Contributor
* Peter Nguyen (PeterNg15): Contributor

# License

* To be filled out
