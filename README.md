<p align="center">
  <img src="favicon.ico" alt="MouseLogger Logo"/>
</p>

# Mouselogger
This `kivy` application logs the mouse dynamics of the user (movement, clicks, scrolling).

Using `kivyMD` and `pynput` the app collects the data and uploads it to our server.
We are a small dev team using data for our student research paper.

Feel free to fork our repo or use the [released application](https://github.com/Studienarbeit-Mouse-Dynamics-DHBW-FN/MouseLogger-App/releases/tag/v1.0.0) to help us in our research.
<br><br>
## Data Collection
We save the mail address you enter in our application and will send you a mail for confirmation. Using the `getmac` package, we will **save our mac and mail address on our servers** to identify your device in our research.

### What we save:
- the location of our cursor in set intervals
- the direction of your scrolling with a timestamp
- the position, time and duration of your clicks

### What we **don't** save:
- what applictions are running on our device
- what websites you're visiting
- any other inputs (e.g. keyboard, audio, etc.)
<br><br>
## Releases
Releases this far:
- [v1.0.0 - **Initial Release**](https://github.com/Studienarbeit-Mouse-Dynamics-DHBW-FN/MouseLogger-App/releases/tag/v1.0.0)
<br><br>
## Requirements
The `python` requirements can be found in the [`requirements.txt`](https://github.com/Studienarbeit-Mouse-Dynamics-DHBW-FN/MouseLogger-App/blob/main/requirements.txt)
<br><br>
## Build app
To build the app under windows, just run: <br>
`pyinstaller main.spec`
<br><br><br>
To build the app under Linux, just run: <br>
`pyinstaller --onefile main.py` <br>
(BEWARE: This changes the `main.spec` with is used for the windows build.)