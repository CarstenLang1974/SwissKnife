import platform
from pathlib import Path
import logging
log = logging.getLogger(__name__)
import MainView

class Controller(object):
    def __init__(self, model):
        self._model = model
        self._screen = MainView.MainView(self._model)
        self._screen.show()
