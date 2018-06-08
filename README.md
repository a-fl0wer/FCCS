![alt text](https://fccs.ml/wp-content/uploads/2017/11/overlay-logo.png)

Fire Command & Control Systems
===


Description of survbot.py
---


The purpose of survbot.py is to
periodically take photos for analysis of the forest while communicating the
results to the FCCS Database. In each iteration the analysis scans the photograph using
the YOLO CNN to detect any possible fire and/or smoke in the vicinity.
If the status of the forest is safe then the device sends only info about its
own functionality, but if the scan detects a fire or smoke object in the
photograph then the device additionally sends the photograph and its detection
rectangles along with their respective labels.


---

**Installation:**

1. Install OpenCV for python2
2. Install Darknet following the installation instructions from https://pjreddie.com/darknet/install/ (assuming you'll clone it at /home/$USER)
3. Clone FCCS
```
cd ~
git clone https://github.com/a-fl0wer/FCCS.git
```
4. Copy the modified version of darknet.py to darknet/python replacing the
original one
```
cp ~/FCCS/darknet.py ~/darknet/python
```
5. Create a soft link on darknet/python pointing at darknet/data directory (or
wherever your data directory is at)
```
ln -s ~/darknet/data ~/darknet/python
```
6. Run survbot.py
```
python survbot.py
```
