# Computer Vision - Game Controller

Game controller using webcam made with computer vision - Python and openCv

![alt text](.//images/test.gif)

## Requirements

- [Python 3](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [Matplotlib](https://matplotlib.org/)
- [Numpy](https://numpy.org/)

Install requirements:
```
pip install -r requirements.txt
```

<br>

## Get Started

- Script file using webcam `gameController.py`

```
python gameController.py
```

- Notebook explaing the functions `notebook/gameControllerNotebook.ipynb`

<br>

## Actions

### Keys

``` py
keys = {
    'A': pynput.keyboard.KeyCode.from_char('a'),  
    'D': pynput.keyboard.KeyCode.from_char('d'),  
    'W': pynput.keyboard.KeyCode.from_char('w'),  
    'S': pynput.keyboard.KeyCode.from_char('s'),  
}
```


**A** = ⬅
- Pressed when angle is positive

**D** = ➡
- Pressed when angle is negative

**W** = ⬆
- Pressed when mass is bigger than 5000

**S** = ⬇
- Pressed when mass is less than 3000

<br>

## Controller Image
You have to use this image to control your car (or horse):

![Volante](./images/steeringwheel.jpeg)

#### Image avaiable on [`./images/steeringwheel.jpeg`](./images/steeringwheel.jpeg)

<br>

---

Developed by [Jean Jacques](https://github.com/jjeanjacques10/) and [Gabriel Petillo](https://github.com/gspetillo/)