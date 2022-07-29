import logging
import os
import src.logger.config as cfg
from src.logger.config import TargetType


def init_logger(target: TargetType):
    if not os.path.exists(cfg.LOG_FOLDER):
        os.mkdir(cfg.LOG_FOLDER)

    if target == TargetType.BOT:
        logging.basicConfig(level=cfg.LOG_BOT_LEVEL)
        file_handler = logging.FileHandler(os.path.join(cfg.LOG_FOLDER, cfg.LOG_BOT_FILE))
        file_handler.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))
        file_handler.setLevel(cfg.LOG_BOT_LEVEL)
        logging.getLogger('').addHandler(file_handler)
    elif target == TargetType.ADMIN:
        logging.basicConfig(level=cfg.LOG_ADMIN_LEVEL)
        file_handler = logging.FileHandler(os.path.join(cfg.LOG_FOLDER, cfg.LOG_ADMIN_FILE))
        file_handler.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))
        file_handler.setLevel(logging.INFO)
        logging.getLogger('').addHandler(file_handler)
    else:
        raise ValueError('Invalid value of target (should be BOT or ADMIN')
