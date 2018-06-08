FCCS
===

+Description of darknet.py:
The purpose of this modified version of darknet.py is to periodicaly
photograph and analyse the forest while communicating the results to the FCCS
Database. Each analysis scans the photograph using the YOLO CNN to detect any
possible fire and/or smoke in the vicinity. In each iteration if the status of
the forest is safe then the device sends only info about its own functionality,
but if the scan detects a fire or smoke object in the photograph then the
device additionaly sends the photograph and its detection rectangles along
with their respective labels.
