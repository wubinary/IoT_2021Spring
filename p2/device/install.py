import os, sys

# Install arduino-cli
os.system('curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/bin sh')

# Configure arduino-cli
os.system('arduino-cli config init')

# Update the core.
os.system('arduino-cli core update-index')

# Add Arduino AVR cores.
os.system('arduino-cli core install arduino:avr')

# Install watchdog
os.system('sudo apt-get install watchdog')
