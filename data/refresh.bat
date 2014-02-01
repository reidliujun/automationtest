adb root
adb remount
adb shell rm -r /data/test_env
adb push test_env     /data/test_env/
adb shell python  /data/test_env/test_main.py

pause
