'''
    wrapper for communicate with uiautomator server.

    This is the wrapper to provide low level communicate
    with the server which performs ui detections and operations.

    The QSST python framework play as a client which communicate
    with uiautomator which play as a server. The communication
    between them now is socket, which implement in this file.

    1.The api provide by this file is used for qsst python framework,
    do not use it directly in cases.

    2.This file contains socket communication with server side(uiautomator),
    if you want add/modify it , I recommand you understand both side enough.

   @author: U{zhibinw<zhibinw@qti.qualcomm.com>}
   @version: version 1.0.0
   @requires:python 2.7+
   @license:

   @see: U{uiautomator<developer.android.com/tools/help/uiautomator>}
   @note:
   @attention:
   @bug:
   @warning:

'''
import socket
import sys
import time
import os
import thread
from logging_wrapper import log_test_framework
from platform_check import get_platform_info

NEW_LINE_TAG = "\n"

class SocketUtil:
    '''
    This class implement low level socket communication with server side(uiautomator).
    in its constructor it try to connect with the given socke_name, send message to
    server side and get response message from server side, close function will close
    the connection.

    To enable develop case on PC , when running case on PC, it will forward
    localhost:6100 to remote socket myuiautomator on device. Running case
    on device will connect myuiautomator socket directly.
    '''

    def __init__(self, local_socket_name, port):
        '''
        Initialize the SocketUtil Instance  by passing local socket name.
        For Windows and Linux-PC , it will connect localhost:6100 since this
        port will forward to remote socket myuiautomator on device. For running
        on Linux-Phone , it will connect to socket myuiautomator directly.

        @type local_socket_name:string
        @param local_socket_name: name of socket.
        @port port:port of socket.
        '''
        osInfo = get_platform_info()
        try:
            if(osInfo == 'Windows' or osInfo == 'Linux-PC'):
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(('127.0.0.1', port))
                self.fd = self.sock.makefile('rw', 0)
            elif(osInfo == 'Linux-Phone'):
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(local_socket_name)
                self.fd = self.sock.makefile('rw', 0)
        except socket.error, msg:
            log_test_framework("io_wrapper", "socket error: " + msg.strerror)
            self.sock = None
            self.fd = None
            raise IOError, 'msg'

    #send a message with new line tag
    def send_msg_line(self, msg):
        '''
        send message to server through socket,end with new line tag. To support multi language,
        It will set encoding to 'utf-8',so plesae make sure your message is encoded in 'utf-8'.

        @type msg:string
        @param msg:message to be sent, encoded in 'utf-8'
        @return: True on success, False on exceptions.
        '''
        if not self.sock:
            return False
        try:
            self.sock.sendall(msg + NEW_LINE_TAG)
        except socket.error, msg:
            log_test_framework("io_wrapper", "socket send error: " + msg.strerror)
            return False
        return True

    #get a response line
    def get_response_line(self, result):
        '''
        get response from server through socket,parase new line tag  as end tag.

        @type result:list
        @param result: result get from the server side.
        @return: True if success, False if exception occurs.
        '''
        if not self.sock:
            return False
        try:
            result[0] = self.fd.readline().strip(NEW_LINE_TAG)
        except IOError, msg:
            log_test_framework("io_wrapper", "socket recv error: " + msg.strerror)
            return False
        return True

    def close(self):
        '''
        close current socket.
        '''
        if not self.sock:
            return
        self.sock.close()
