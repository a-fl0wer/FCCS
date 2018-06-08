Fire Command & Control Systems
===


Description of darknet.py
---


The purpose of this modified version of the original darknet.py (pjreddie) is to
periodically photograph and analyze the forest while communicating the results
to the FCCS Database. Each analysis scans the photograph using the YOLO CNN to
detect any possible fire and/or smoke in the vicinity. In each iteration if the
status of the forest is safe then the device sends only info about its own
functionality, but if the scan detects a fire or smoke object in the photograph
then the device additionally sends the photograph and its detection rectangles
along with their respective labels.

---

**Requirements:**

1. OpenCV for python2
2. Darknet: Follow the installation instructions from https://pjreddie.com/darknet/install/
3. Copy this modified version of darknet.py to darknet/python and replace the
original one
4. Create a soft link on darknet/python pointing at darknet/data directory (or
wherever your data directory is)
```
cd *Installation path*/darknet/python
ln -s darknet/data .
```
5. Run
```
python darknet.py
```
