#!/usr/bin/env python

# System imports
import io
import os

# Configparser imports
import configparser

# Logging imports
import logging

# Globals
configfile_name = "config.ini"

# Check if there is already a configurtion file if not regenerate it
def init_conf():
    if not os.path.isfile(configfile_name):
        logging.warning('Create the configuration file as it doesn\'t exist yet. Factory configuration is applyed.')
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
        
        config.add_section('others')
        config['others']['logging_level'] = 'DEBUG'        

        config.write(cfg_file)
        cfg_file.close()
        logging.warning('Configuration file created.')
    else:
        logging.info('Configuration file present.')
        pass

# Basic config check
def read_conf():
    logging.info('Start parsing configuration file.')
    config = configparser.ConfigParser()
    config.read(configfile_name)
    config_version = config['thermostatPi']['config_version']
    logging.info('Configuration file version: %s', config_version)
    logging.info('Parsing configuration file finished.')

# Function for reading a parameter from configuration file
def read_conf_param(section, param):
    config = configparser.ConfigParser()
    config.read(configfile_name)
    value = config[section][param]
    logging.debug('Read parameter from configuration file: %s[%s] = %s', str(section) , str(param), str(value))
    return value

# Function for write/update a parameter to configuration file
def write_conf_param(section, param, value):
    config = configparser.ConfigParser()
    config.read(configfile_name)
    with open(configfile_name, 'w') as configfile:
        config.set(section, param, value)
        config.write(configfile)
        configfile.close()
        logging.debug('Write parameter to configuration file: %s[%s] = %s', str(section) , str(param), str(value))

