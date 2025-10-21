import os
import configparser

CONFIG = configparser.ConfigParser(allow_no_value=True)
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(DIRECTORY, 'config.conf')
CONFIG.read(CONFIG_FILE_PATH)

def config():
	return CONFIG
