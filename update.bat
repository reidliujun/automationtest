adb root

pause

adb remount

pause

adb push  system /system/

adb push  data   /data/ 


adb shell chmod 4777 /system/bin/python

adb shell chmod 4777 /system/bin/uiautomator

adb shell chmod -R  777 /data/python_env/


adb shell chmod -R  777 /data/test_env/


adb shell chmod 6755 /system/xbin/su
pause
pause

adb shell rm /system/framework/uiautomator.odex
