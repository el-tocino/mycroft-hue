# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import getLogger
from phue import Bridge
from fuzzywuzzy import fuzz

__author__ = 'brihopki'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

def _connect_bridge(bridge):
    # Connecting to bridge
    bridge.connect()
    LOGGER.debug("This is the bridge ip: {}".format(bridge.ip))
    return bridge

def get_group_name(bridge, phrase_group):
    # Getting groups object from the bridge class
    groups = bridge.get_group()
    best_score = 50
    best_group = None
    for line in groups:
        score = fuzz.ratio(phrase_group, groups[line]['name'])
        if score > best_score:
            LOGGER.debug("The score is {}".format(score))
            best_score = score
            group_name = groups[line]['name']
            hue_group = groups[line]
            group_on = groups[line]['state']['any_on']
            group_lights = groups[line]['lights']
    return group_name, group_on, group_lights

def all_lights_on_off(bridge, action):
    all_lights = []
    lights = bridge.lights
    for light in lights:
        all_lights.append(light.name)
    if action == 'on':
        bridge.set_light(all_lights, 'on', True )
        LOGGER.debug("Turning on all lights")
    else:
        bridge.set_light(all_lights, 'on', False)
        LOGGER.debug("Turning off all lights")

def change_group_color(bridge, group, color):
    hue_group = get_group_name(bridge, group)
    LOGGER.debug("This is the hue group: {}".format(hue_group[0]))
    if color == 'red' or color == 'read':
        bridge.set_group(hue_group[0], 'xy', [0.704, 0.296])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    elif color == 'blue':
        bridge.set_group(hue_group[0], 'xy', [0.138, 0.08])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    elif color == 'yellow':
        bridge.set_group(hue_group[0], 'xy', [0.4487, 0.4906])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    elif color == 'purple':
        bridge.set_group(hue_group[0], 'xy', [0.2217, 0.1126])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    elif color == 'green':
        bridge.set_group(hue_group[0], 'xy', [0.409, 0.518])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    else:
        bridge.set_group(hue_group[0], 'xy', [0.3107, 0.3288])
        LOGGER.debug("Setting group {} to color {}".format(hue_group[0], color))
    return hue_group[0]



# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class GeekHueSkill(MycroftSkill):
    def __init__(self):
        super(GeekHueSkill, self).__init__(name='GeekHueSkill')
        self.ip = self.config.get('bridge_ip')
        self.bridge = Bridge(self.ip)

    @intent_handler(IntentBuilder('GroupColorIntent').require("GroupColorKeyword").require('Group').require('Color').build())
    def handle_group_color(self, message):
        color = message.data['Color']
        group = message.data['Group']
        LOGGER.debug("The color is {} the group is {}.".format(color, group))
        bridge = _connect_bridge(self.bridge)
        color_group = change_group_color(bridge, group, color)
        self.speak("Changed the {} to color {}".format(color_group, color))


    @intent_handler(IntentBuilder('GroupLightIntent').require("GroupLightKeyword").require('Action').require('Group').build())
    def handle_group_light(self, message):
        phrase_group = message.data['Group']
        action = message.data['Action']
        LOGGER.debug("This is the bridge info: {}".format(self.bridge))
        bridge = _connect_bridge(self.bridge)
        if phrase_group == 'all lights':
            all_lights_on_off(bridge, action)
            self.speak("Turned {} all lights".format(action))
        else:
            group = get_group_name(bridge, phrase_group)
            group_on = group[1]
            group_name = group[0]
            group_lights = group[2]
            group_id = ''
            if action == 'on':
                if group_on == False:
                    LOGGER.debug("The group we would turn {} is {}".format(action, group_name))
                    group_id = bridge.get_group_id_by_name(group_name)
                    bridge.set_group(group_name, 'on', True)
                    self.speak("Turned {} group {}".format(action, group_name))
                else:
                    LOGGER.debug("Group {} is already {}".format(group_name, action))
                    self.speak("Group {} is already {}".format(group_name, action))
            else:
                if group_on == True:
                    LOGGER.debug("The group we would turn {} is {}".format(action, group_name))
                    group_id = bridge.get_group_id_by_name(group_name)
                    bridge.set_group(group_name, 'on', False)
                    self.speak("Turned {} group {}".format(action, group_name))
                else:
                    LOGGER.debug("The group {} is already {}".format(group_name, action))
                    self.speak("Group {} is already {}".format(group_name, action))

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return GeekHueSkill()
