import copy
from copy import Error
from mock import patch
from pywinauto import Desktop
import shelve
from shelve import BsdDbShelf
import themcontrols
from themcontrols import Controls
from themcontrols import Expresions
import unittest


class ThemcontrolsTest(unittest.TestCase):
    @patch.object(BsdDbShelf, '__setitem__')
    @patch.object(copy, 'copy')
    def test_add(self, mock_copy, mock___setitem__):
        mock_copy.return_value = {'parent': 'Desktop 1', 'auto_id': '', 'title': 'Taskbar', 'class_name': 'Shell_TrayWnd', 'control_type': 'Pane', 'control_id': 0, 'handle': 196650, 'framework_id': 'Win32', 'backend': 'uia'}
        mock___setitem__.return_value = None
        self.assertEqual(
            Controls.add(self=<themcontrols.Controls object at 0x000001486E925D90>,cid='a6bf8ef99faf',obj=<uiawrapper.UIAWrapper - '', Pane, 8845848544669407285>,searchcrit={'parent': 'Desktop 1', 'auto_id': '', 'title': '', 'windowtext': '', 'class_name': 'MSO_BORDEREFFECT_WINDOW_CLASS', 'control_type': 'Pane', 'control_id': 0, 'handle': 1247890, 'processid': 4440, 'framework_id': 'Win32', 'backend': 'uia', 'rectangle': <RECT L718, T342, R726, B698>, 'visible': True, 'children': 0}),
            None
        )


    def test_get(self):
        self.assertIsInstance(
            Controls.get(self=<themcontrols.Controls object at 0x000001486E925D90>,id='3f2ed6399238'),
            pywinauto.controls.uiawrapper.UIAWrapper
        )


    def test_is_in(self):
        self.assertEqual(
            Expresions.is_in(self=<themcontrols.Expresions object at 0x0000014872ED16D0>,sourcestr='3f2ed6399238',sourcedict=dict_keys(['bb33e9ad94c2', 'ab79acd2005c', '78103ea67688', 'a1d7b4ba6383', '3f2ed6399238', 'a6bf8ef99faf', '591db0e07b9a', '67d3325514ff', '24acbd75e7f1', '1d650fc24606', '5ae9999a18c8', 'f2c010b97137', '24683dcab7ca', 'f52257eee5f7'])),
            True
        )


if __name__ == "__main__":
    unittest.main()
