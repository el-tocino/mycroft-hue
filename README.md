# Geek Hue skill

This skill is a revamp of @btothayre's hue skill using fuzzy matching for adjusting lights, groups, and colors.  (Should work with python 3 now as well?)


# Installation/Setup
1. msm install GITHUBURL HERE
2. go to home.mycroft.ai and the skills and add your hue hub ip.


## Current state

Working features:
 - Currently can turn on and off groups by saying anything like below replacing with your group name.
    - turn on office
    - turn off office
    - switch on office
    - switch off office
    - turn on all lights
    - turn off all lights

 - Can change to the below colors currently by saying "Change/Set Office(Groupname) blue(Color)" or "Change/Set Office(Groupname) to blue(Color)".  

 - Supports webcolors names, ie, Chuck Norris, blue, light blue, mauve, taupe, etc.

 - Lights can now be adjusted by name! 

Known issues:
 - ...

TODO:
 - Auto discovery of hue bridge
 - Scenes on and off by name
 - Give you back list of groups then you can say which one you want to turn on/off
