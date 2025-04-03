# 📸 PixelPlanet Timelapser

[![License](https://img.shields.io/badge/License-WTFPL-brightgreen)](https://www.wtfpl.net/)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/Hype0290/timelapse-bot-pixelplanet?style=social)](https://github.com/Hype0290/timelapse-bot-pixelplanet/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Hype0290/timelapse-bot-pixelplanet?style=social)](https://github.com/Hype0290/timelapse-bot-pixelplanet/network)

This is a Python tool that downloads changes on the canvas in real-time, without using the history mode.

---

### ⚡ TODO

[✅] Add option to show the time on the frames



---

## ⚙️ Usage

### Fetch and Save Timelapse Frames
```bash
python3 timelapser.py startX_startY endX_endY canvasID website [no_compare] [timestamp]
```
- `startX_startY`: Starting coordinates of the area (e.g., `100_200`).
- `endX_endY`: Ending coordinates of the area (e.g., `300_400`).
- `canvasID`: ID of the canvas to fetch data from.
- `website`: PixelPlanet clone website (e.g., `pixelplanet.fun`).
- `[no_compare]`: Optional. Add this to save all frames, even if no pixel changes are detected.
- `[timestamp]`: Optional. Add this to add a timestamp to each frame.
### List Available Canvases
```bash
python3 timelapser.py canvases "website"
```
- `website`: PixelPlanet clone website to fetch canvas information.

### Display Help
```bash
python3 timelapser.py -h
```

---

## 🖥️ Example

To create a timelapse of a specific area:
```bash
python3 timelapser.py 100_200 300_400 0 pixelplanet.fun
```

To list available canvases:
```bash
python3 timelapser.py canvases "pixelplanet.fun"
```

To create a video from saved frames using `ffmpeg`:
```bash
ffmpeg -framerate 60 -f image2 -i frame/t%d.png -c:v libvpx-vp9 -pix_fmt yuva420p timelapse.mp4
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- `pip` (Python package manager)
- `ffmpeg` (for creating videos from frames)

### Install on Linux

#### Debian/Ubuntu
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
pip3 install -r requirements.txt
```

#### Fedora
```bash
sudo dnf install python3 python3-pip ffmpeg
pip3 install -r requirements.txt
```

#### Arch Linux
```bash
sudo pacman -S python python-pip ffmpeg
pip3 install -r requirements.txt
```

### Install on Windows

1. Download and install [Python](https://www.python.org/downloads/) (ensure to check "Add Python to PATH" during installation).
2. Download and install [ffmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.
3. Open Command Prompt and run:
    ```cmd
    pip install -r requirements.txt
    ```

---

## 📜 License

This project is licensed under the [WTFPL License](https://opensource.org/licenses/WTFPL). See the `LICENSE` file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

## 📧 Contact

For questions or feedback, please reach out to the project maintainer: [Hype0290](https://github.com/Hype0290)
