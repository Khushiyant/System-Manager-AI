# System Manager AI

It is python program that can execute commands via voice input.

## Installation

Use git clone to install System Manager AI.

```bash
git clone https://github.com/Khushiyant/System-Manager-AI.git
```
## Requirement
```bash
pip install SpeechRecognition
pip install pyttsx3
pip install pyaudio
pip intall google
pip install bs4
pip install requests
```

if you have problem installing pyaudio, download .whl according to your python version from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## Usage

```python
import features
cmd = features.takeCommand()
cmd = cmd.lower()
features.commandCenter(cmd)
```
or 

simply run master.pyw

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
