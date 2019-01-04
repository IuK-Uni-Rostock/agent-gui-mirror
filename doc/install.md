# Installation on Raspberry Pi (any model)

## 1. Install dependencies
1. Install GIT and Python3 package manager pip3 `sudo apt install git python3-pip`
2. Install PyQt5 `pip3 install pyqt5`

## 2. Install agent-gui
1. Switch to home directory `cd ~`
2. Download agent-gui `git clone --recurse-submodules https://git.informatik.uni-rostock.de/iuk/security-projects/software/building-automation/agent-gui.git`
3. Follow instructions to install agent located at `agent-gui/agent/doc/install.md`

## 3. Install fbcp (used to mirror primary framebuffer to secondary framebuffer)
1. Switch to rpi-fbcp directory `cd agent-gui/tools/rpi-fbcp`
2. Compile `mkdir build && cd build && cmake .. && make`
3. `sudo cp fbcp /usr/local/bin`
4. Fix framebuffer width: `sudo sed -i -e 's/#framebuffer_width=.*/framebuffer_width=1920/g' /boot/config.txt`
5. Fix framebuffer height: `sudo sed -i -e 's/#framebuffer_height=.*/framebuffer_height=1080/g' /boot/config.txt`
6. Enable spi module: `sudo echo 'spi-bcm2835' >> /etc/modules`
7. Enable fbtft module: `sudo echo 'fbtft_device' >> /etc/modules`
8. Copy fbtft device configuration: `sudo cp agent-gui/doc/fbtft.conf /etc/modprobe.d`
9. Reboot `sudo reboot`

## 4. Keep display active
1. `sudo sed -i -e 's/#xserver-command=X/xserver-command=X -s 0 dpms/g' /etc/lightdm/lightdm.conf`

## 5. Add to autostart
1. Switch to home directory `cd ~`
2. `cp agent-gui/doc/fbcp.service ~/.config/systemd/user` (it might be necessary to create the directory first)
3. `cp agent-gui/doc/xsession.target ~/.config/systemd/user`
4. Reload systemd `systemctl --user daemon-reload`
5. Enable fbcp systemd service `systemctl --user enable fbcp.service`
6. Enable autostart of all our created systemd services: `echo '@systemctl --no-block --user start xsession.target' >> ~/.config/lxsession/LXDE-pi/autostart`
7. Enable autostart of agent-gui: `sudo cp agent-gui/doc/agent-gui.desktop /etc/xdg/autostart`
