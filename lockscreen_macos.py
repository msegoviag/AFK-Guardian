from ctypes import CDLL


class LockScreen:

    def lockscreenMacOS():
        loginPF = CDLL(
            '/System/Library/PrivateFrameworks/login.framework/Versions/Current/login')
        result = loginPF.SACLockScreenImmediate()

    def lockcreenWindows():
        pass

    def lockscreenLinux():
        pass
