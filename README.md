# Geek Hue skill

This skill is a revamp of the existing hue skill using fuzzy matching for turning groups on and colors eventually, etc.

To get this done we need
  - phue

# Installation/Setup
1. Modify your mycroft.conf file and add the following section replacing with your hue bridge IP:
```
"GeekHueSkill": {
  "bridge_ip": "X.X.X.X"
 }
```
2. msm install https://github.com/Geeked-Out-Solutions/mycroft-hue.git


## Current state

Working features:
 - Currently can turn on and off groups by saying anything like below replacing with your group name.
    - turn on office
    - turn off office
    - switch on office
    - switch off office
    - turn on all lights
    - turn off all lights

Known issues:
 - ...

TODO:
 - Auto discovery of hue bridge
 - Scenes on and off by name
 - Lights on and off by name
 - Give you back list of groups then you can say which one you want to turn on/off
 - Change to colors red, green, etc.
