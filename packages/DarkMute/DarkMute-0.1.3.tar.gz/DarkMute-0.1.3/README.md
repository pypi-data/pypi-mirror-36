# Dark Mute

Dark Mute is python script that mutes snapcast client volume 
when it senses lights are off in the room.

It's written in Python 3 and requires a  photoresistor-capacitor circuit 
connected to a Raspberry Pi running Snapcast.

# Setup/Usage

As the `pi` user in its home directory:

* `python3 -m venv darkmute-venv`
* `. darkmute-venv/bin/activate`
* `sudo python3 -m pip install DarkMute`

To run this as a service, create a systemd service definition. Instructions pending.

# Developer Setup

* Clone this from [gitlab](https://git.xhost.io/jess/Dark-Mute)
* Create and activate Python 3 virtual env
* `pip install -e .` to install dependencies
* Build the circuit, connected to GPIO Pin 7 
* add user to gpio group [/dev/gpiomem](https://raspberrypi.stackexchange.com/a/40106)  
