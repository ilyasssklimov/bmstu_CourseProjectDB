from config import LOG_FOLDER, LOG_NAME_FILE
import logging
import os


def init_logger():
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)

    logging.basicConfig(level='INFO')
    file_handler = logging.FileHandler(os.path.join(LOG_FOLDER, LOG_NAME_FILE))
    file_handler.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))
    file_handler.setLevel(logging.INFO)
    logging.getLogger('').addHandler(file_handler)
