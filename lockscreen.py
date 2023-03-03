import os
import ctypes
from ctypes import CDLL

class LockScreen:

    @staticmethod
    def lockscreen_macos():
        loginPF = CDLL(
            '/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
        loginPF.SACLockScreenImmediate()
    
    @staticmethod
    def lockscreen_windows():
        ctypes.windll.user32.LockWorkStation()

    @staticmethod
    def suspend_windows():
        powrprof = ctypes.windll.LoadLibrary('powrprof.dll')
        powrprof.SetSuspendState(0, 1, 0)

    @staticmethod
    def off_windows():

        EWX_LOGOFF = 0x00000000
        EWX_FORCE = 0x00000004
        EWX_POWEROFF = 0x00000008
        EWX_REBOOT = 0x00000002
        EWX_SHUTDOWN = 0x00000001

        # Llamada a correspondiente que efectua la operación
        ctypes.windll.user32.ExitWindowsEx(EWX_LOGOFF | EWX_FORCE, 0)

    # Works on Ubuntu: testing in 22.04
    @staticmethod
    def lockscreen_linux():
        os.system('xdg-screensaver activate && xdg-screensaver lock')
