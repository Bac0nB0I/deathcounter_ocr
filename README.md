# deathcounter_eldenring_ocr

A python script which detects death messages for Elden Ring by using *O*ptical *C*haracter *R*ecognition.
The number of deaths is then displayed in a graphical user interfaces. The number of deaths is saved between sessions. <br/>
The deathcounter doesn't interact with the game in any way and is therefore _compatible_ with _online play_. <br/>
The deathcounter can be used for counting your deaths while livestreaming or just for yourself. <br/>
In my tests there was _no noticable performance impact_.

<br /><br />

# How does it work?

Every 0.75 seconds the script takes a screenshot of your screen. The image gets cropped so that it only consists of the part of the screen where the death message appears. A mask corrosponding to the color of the death message gets generated. The mask is turned grayscale. After that the black and white values get filtered to be more readable for the OCR Algorithm. The processed image is then passed to the OCR algorithm and the result is passed to the counter.

# Requirements:

## 1) Install Python 3

As this is a python script you need a working python installation on your machine.
You can install the required version of python 3 from the [official website](https://www.python.org/downloads/) or download it from the microsoft store which is easier as is also installs pip.

## 2) Install Tesseract OCR

Install a version of _Tesseract OCR_ [(Download)](https://github.com/UB-Mannheim/tesseract/wiki) <br/>
You only need the english language package, all of the other available things you can choose are not necessary

## 3) Install required pip libraries

```console
pip install pytesseract
pip install PyAutoGUI
pip install opencv-python
```

## 4) Change set location of Tesseract OCR installation

In _config.json_ you have to change the path to tesseract.exe so that it matches the setup on your machine("tesseract_directory": "YOUR_PATH"). Remember to double every \*\*

# Usage

Use the following command while having a Command Line Interface open in the directory the script is located:

```console
python deathcounter.py
```

or

```console
py deathcounter.py
```

If you want to show the counter while streaming you just have to add the window which displays the counter as a source in OBS.<br/>
You can activate the compact_mode with the parameter "enable" to only show the number of deaths in the displayed window. This can be useful if you want to use it as an OBS source and not use that much space for it <br/>
You can acitvate the debug_mode with the parameter "enable" in config.json to see debug info and maybe try to improve the image processing yourself <br/>

# config.json

| Name                    | Values            | Usage                                                                                                                         |
| ----------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| "tesseract_directory":  | directory path    | Use this to set the path to the directory your tesseract.exe is installed in                                                  |
| "refresh_time":         | time in ms        | Use this to configure the time the program waits between taking screenshots. Lower values lead could lead to better detection |
| "refresh_time_success": | time in ms        | Same as above but only gets used if a match is successfully detected                                                          |
| "debug_mode":           | enabled/disabled  | Will print debug messages to console and output images for debugging to debugImages\ if enabled                               |
| "compact_mode":         | enabled/disabled  | Will remove all elements of the counter except the number of deaths from the display window if enabled                        |
| "crop_file":            | name/path to file | Use to set the file which contains coodinates where image gets cropped (Standard: crop.json)                                  |

# Known Issues

Sometimes the detection goes wrong, for this reason you can change the counter by changing the content of the deaths.txt file or use the integrated button to manually change the value. <br/>

The script only works if you use the resolution 1920x1080. If you use a different resolution you have to change the image crop coordinates, which can be configured by using the python script provided in debugImages\ and the config to crop out the correct part of the screen. <br/>

Currently only works with the english version of the game. <br/>
