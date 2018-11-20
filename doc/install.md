# Installation on Raspberry Pi (any model)

## 1. Install dependencies
1. Install GIT and Python3 package manager pip3 `sudo apt install git python3-pip`
2. Install PyQt5 `pip3 install pyqt5`

## 2. Install agent-gui
1. Switch to home directory `cd ~`
2. Download agent-gui `git clone --recurse-submodules https://git.informatik.uni-rostock.de/iuk/security-projects/software/sindabus-agent-gui.git`
3. Follow instructions to install agent located at `sindabus-agent-gui/agent/doc/install.md`

## 3. Install fbcp (used to mirror primary framebuffer to secondary framebuffer)
1. Switch to rpi-fbcp directory `cd sindabus-agent-gui/tools/rpi-fbcp`
2. Compile `mkdir build && cd build && cmake .. && make`
3. `sudo cp fbcp /usr/local/bin`

## 4. Keep display active
1. `sudo sed -i -e 's/#xserver-command=X/xserver-command=X -s 0 dpms/g' /etc/lightdm/lightdm.conf`

## 5. Add to autostart
1. Switch to home directory `cd ~`
2. `cp sindabus-agent-gui/doc/fbcp.service ~/.config/systemd/user` (it might be necessary to create the directory first)
3. `cp sindabus-agent-gui/doc/xsession.target ~/.config/systemd/user`
4. Reload systemd `systemctl --user daemon-reload`
5. Enable fbcp systemd service `systemctl --user enable fbcp.service`
6. Enable autostart of all our created systemd services: `echo '@systemctl --no-block --user start xsession.target' >> ~/.config/lxsession/LXDE-pi/autostart`
7. Enable autostart of agent-gui: `sudo cp sindabus-agent-gui/doc/agent-gui.desktop /etc/xdg/autostart`
