# *IRDecoder*

This is a work in progress. 
If you would like to help you are more then welcome to.

#### ***Background***

---
I have not been able to locate a cross platform IR library for Python. Most of the libraries available are for posix. I have not found any Python library that capable of handling Windows MCE remotes.
WinLirc is no longer being developed and had a very minimal number of protocols and device support in it.
I also wanted a library that did all of the heavy lifting without relying on extension modules or other applications.

I came across IRremoteESP8266 which has a plethora of protocols it is able to handle and the code seemed reasonably easy to follow, tho it is written in cpp.
I have already written all of the Windows API bindings needed to interface with an MCE device, and porting the IRremoteESP8266 code to Python is not all that hard of a task
(wrote a program that did most of the work!!!)


#### ***Description***

---
Port of IRremoteESP8266 by @crankyoldgit to Python (https://github.com/crankyoldgit/IRremoteESP8266). 
This library was originally based on Ken Shirriff's work (https://github.com/shirriff/Arduino-IRremote/)  
Mark Szabo has updated the IRsend class to work on ESP8266 and Sebastien Warin the receiving &amp; decoding part (IRrecv class).

#### ***Goals***

---
When finished this library will support sending and receiving on Windows using an MCE transmitter/receiver (ehome usbcir driver)
It will also work with several of the more popular serial/USB transmitters/receivers.
It will be able to be run on an ESP8266 and ESP32 that is running MicroPython.
I may add bindings to lirc for Posix users. 
