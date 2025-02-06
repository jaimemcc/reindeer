# reindeer
Scripts etc for analysing reindeer data

This repo currently has a function that is useful for converting files of reindeer behaviour captured in the field.

## Installation
1. Install tesseract, e.g. from https://github.com/UB-Mannheim/tesseract/wiki

When you install keep track of where `tesseract.exe` ends up on your computer as you will need to replace this path in the .py script.

2. Install ffmpeg (if you don't already have it)

Easiest (on Windows) is to run `winget install ffmpeg` as it will also add it to your environment path.

3. Clone the reindeer repository

Open an Anaconda/Miniconda command prompt and run
```
git clone https://github.com/jaimemcc/reindeer.git
```

4. Create a new environment from the `environment.yml` file

Navigate to `reindeer` folder and run the following command

```
conda env create -f environment.yml
```

5. Tell the script where to find your Tessearct installation

Open the file `scripts/videoresize.py` and change the following line so that it points to you version of `tesseract.exe`. It will probably look similar to the one that is already there. If you have doubts or struggle to find it, you can always restart the installer file as it will show you where it's going to install.
```
pytesseract.pytesseract.tesseract_cmd = r'C:\\your\\file\\path\\Tesseract-OCR\\tesseract.exe'
```

6. Run the script `scripts/videoresize.py`

Navigate to the `scripts` folder, if not already there, and run a line such as the following to process either a whole directory or a single file.
```
python videoresize.py -d C:/Users/reindeer/data -o C:/Users/reindeer/results -c SALT
```
or
```
python videoresize.py -f C:/Users/reindeer/data/video1.MP4 -o C:/Users/reindeer/results -c SHELLS
```
can also include the `scale` argument (`-s` or `--scale`) to reduce the size of videos even more. Default is 0.5.

