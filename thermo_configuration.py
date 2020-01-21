#!/usr/bin/env python

import configparser
import io
import os

configfile_name = "config.ini"


# Check if there is already a configurtion file
def init_db():
    if not os.path.isfile(configfile_name):
        print("Create the configuration file as it doesn't exist yet")
        cfg_file = open(configfile_name, 'w')

        config = configparser.ConfigParser()

        config.add_section('thermostatPi')
        config['thermostatPi']['version'] = '1.0'
        config['thermostatPi']['config_version'] = '1.0'

        config.add_section('week_prog')
        config['week_prog']['sun'] = '0.0.0.0.0.1.0.0'
        config['week_prog']['mon'] = '0.0.0.0.0.1.0.0'

        config.add_section('global_settings')
        config['global_settings']['hysteresis'] = '5'

        config.write(cfg_file)
        cfg_file.close()
    else:
        print("Configuration file ok")
        pass


def read_conf():
    config = configparser.ConfigParser()
    config.read(configfile_name)

    config_version = config['thermostatPi']['config_version']

    print(f'Configuration file version: {config_version}')


def read_conf_param(section, param):
    config = configparser.ConfigParser()
    config.read(configfile_name)

    value = config[section][param]

    print(f'Read from configuration file: {section} {param} {value}')

    return value


def write_conf_param(section, param, value):
    config = configparser.ConfigParser()
    config.read(configfile_name)

    with open(configfile_name, 'w') as configfile:
        config.set(section, param, value)
        config.write(configfile)
        configfile.close()
        print(f'Write to configuration file: {section} {param} {value}')