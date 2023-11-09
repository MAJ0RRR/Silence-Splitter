# Skrypt usuwający ciszę w nagraniach
## Projekt na Usługi i Aplikacje Multimedialne 2023


### Setup 

Create virtual enviroment in root folder of the repository:
```
python -m venv .venv
```
Activate virtual enviroment:
```
cd .venv/bin && source activate && cd ../..
```
Install requirements:
```
pip install -r requirements.txt
```

### Script

Create 3 folders in root folder of the cloned repository: <br>
    - `input` : There goes original .mp3 file <br>
    - `output` : There will be slices of original audio slcied at moments of silence <br>
    - `joined` : There will be .mp3 file glued together from chunks <br>

You can run the script with default parameters:
```
python3 main.py
```

There are also CLI arguments you can pass to script: <br>
    - `-t` Thresholds below which audio is considered silent. Default: [-45]. <br>
    - `-l` Lengths of silence in miliseconds on which splitting happens. Default: [300]. <br>
    - `-s` Source folder (input) <br>
    - `-d` Destination folder (output)
