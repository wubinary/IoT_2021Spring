import os

# Check
project = 'ring'
if not os.path.isdir(project):
    os.system('arduino-cli sketch ring')

# Compile
os.system('arduino-cli compile -b arduino:avr:uno ring')

# Upload
command_str = f'arduino-cli -v upload -p /dev/ttyACM0 --fqbn arduino:avr:uno ring'
os.system(command_str)

