
from pywinauto.win32_hooks import Hook
from pywinauto.win32_hooks import KeyboardEvent
from pywinauto.win32_hooks import MouseEvent

class themhook():
    hook = Hook()

    def __init__(self):
        self.hook.handler = self.proc_events

    def proc_events(self, args):
        if isinstance(args, KeyboardEvent):
            print('Keyboard Cur:',args.current_key)
            print('Keyboard Type:', args.event_type)
            print('Keyboard All:', args.pressed_key)
            print('----')
        if isinstance(args, MouseEvent):
            print('Mouse Cur:',args.current_key)
            print('Mouse Type:',args.event_type)
            print('Mouse X:',args.mouse_x)
            print('Mouse Y:',args.mouse_y)
            print('----')

    def start(self):
        self.hook.hook(keyboard=True, mouse=True)
        print('Started Recording')
    def stop(self):
        self.hook.unhook_keyboard()
        self.hook.unhook_mouse()
        print('stopped Recording')