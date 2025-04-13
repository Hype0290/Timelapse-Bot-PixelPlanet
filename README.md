# 📸 PixelPlanet Timelapser  
> *(Might work weirdly on PixelPlanet, but works well on its clones)*  

<p align="center">
  <a href="https://www.wtfpl.net/"><img alt="License" src="https://img.shields.io/badge/License-WTFPL-brightgreen"></a>
  <a href="https://www.python.org/"><img alt="Python Version" src="https://img.shields.io/badge/python-3.7%2B-blue.svg"></a>
  <a href="https://github.com/Hype0290/timelapse-bot-pixelplanet/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Hype0290/timelapse-bot-pixelplanet?style=social"></a>
  <a href="https://github.com/Hype0290/timelapse-bot-pixelplanet/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/Hype0290/timelapse-bot-pixelplanet?style=social"></a>
</p>

---

## 📦 About

This is a Python tool that downloads canvas changes in real-time, without using history mode.

---

## ⚡ TODO

- [x] Add option to show the time on the frames  
- [ ] Add a GUI or something to be used easily (for dumbasses)

---

## ⚙️ Usage

### 📥 Fetch and Save Timelapse Frames
```bash
python3 timelapser.py startX_startY endX_endY canvasID website [no_compare] [timestamp]
```
- `startX_startY`: Starting coordinates (e.g., `100_200`)
- `endX_endY`: Ending coordinates (e.g., `300_400`)
- `canvasID`: Canvas ID (usually `0`)
- `website`: PixelPlanet clone domain (e.g., `pixelplanet.fun`)
- `[no_compare]`: *(optional)* Save all frames, even without pixel changes
- `[timestamp]`: *(optional)* Add timestamps to frames

### 🗺️ List Available Canvases
```bash
python3 timelapser.py canvases "website"
```

### 📖 Help
```bash
python3 timelapser.py -h
```

---

## 🖥️ Example

Record a timelapse of a zone:
```bash
python3 timelapser.py 100_200 300_400 0 pixelplanet.fun
```

List canvases:
```bash
python3 timelapser.py canvases "pixelplanet.fun"
```

Create a video with `ffmpeg`:
```bash
ffmpeg -framerate 60 -f image2 -i frame/t%d.png -c:v libvpx-vp9 -pix_fmt yuva420p timelapse.mp4
```

---

## 🛠️ Installation

### Requirements
- Python 3.7+
- `pip` (Python package manager)
- `ffmpeg` (for video generation)

### 🐧 Linux

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

### 🪟 Windows

1. Install [Python](https://www.python.org/downloads/) (make sure to check **"Add Python to PATH"**).
2. Install `ffmpeg` via **winget** in an **Administrator PowerShell or CMD**:
```powershell
winget install ffmpeg
```
3. In CMD or PowerShell:
```cmd
pip install -r requirements.txt
```

---


## 📜 License

This project is licensed under the [WTFPL License](https://opensource.org/licenses/WTFPL).  
See the `LICENSE` file for details.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open issues or submit pull requests 💬

---

## 📧 Contact

Maintained by [**@Hype0290**](https://github.com/Hype0290)
