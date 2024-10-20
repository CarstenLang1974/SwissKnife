import json
import os
import platform
import logging
log = logging.getLogger(__name__)
from PyQt5.QtGui import *
from ProjectModel import ProjectModel

class Model(QStandardItemModel):
    def __init__(self, settings_file):
        """
        init model
        """
        super().__init__()
        settings_file_path=os.path.abspath(settings_file)
        log.debug("load settings file :{}".format(settings_file_path))
        try:
            with open(settings_file) as f:
                self.settings = json.load(f)
            log.debug(self.settings)
        except FileNotFoundError:
            pass
        except Exception as e:
            log.exception(str(e))
