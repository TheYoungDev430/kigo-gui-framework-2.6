from .platform import is_android, android_api_level
from .lifecycle import AndroidLifecycle
from .info import device_info

__all__ = [
    "is_android",
    "android_api_level",
    "AndroidLifecycle",
    "device_info",
]