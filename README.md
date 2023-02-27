# DecontaminatorGui

This is a fork of [TaxIGui](https://github.com/iTaxoTools/TaxIGui),
configured for [Decontaminator](https://github.com/iTaxoTools/Decontaminator).


### Windows and macOS Executables
Download and run the standalone executables without installing Python.</br>
[See the latest release here.](https://github.com/iTaxoTools/DecontaminatorGui/releases/latest)


### Installing from source
Clone and install the latest version (requires Python 3.8.6 or later):
```
git clone https://github.com/iTaxoTools/DecontaminatorGui.git
cd DecontaminatorGui
pip install . -f packages.html
```


## Usage
To launch the GUI, please use:
```
decontaminator-gui
```

Then select one of the available modes and follow the instructions on the screen.


### Packaging

It is recommended to use PyInstaller from within a virtual environment:
```
pip install ".[dev]" -f packages.html
pyinstaller scripts/decontaminator.spec
```
