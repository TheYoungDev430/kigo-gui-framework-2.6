# kigo/android/platform.py
import sys

def is_android():
    return hasattr(sys, "getandroidapilevel")


def android_api_level():
    if is_android():
        return sys.getandroidapilevel()
    return None
	