# Opensubtitles subtitle downloader
Simple python script to automatically download subtitles for every video file found in a folder (recursively). You can also specify a language (available languages can be found [here](https://www.opensubtitles.org/addons/export_languages.php))

# Usage
- Download or clone the repository.
- Edit the `dotenv-sample.txt` with your opensubtitles.com login details.
- Rename `dotenv-sample.txt` to `.env`. (no filename, just the extension like that)
- Install requirements:
```
pip install -r requirements.txt
```
- Run main.py with the correct arguments.

## Program arguments
```
positional arguments:
  path                  The path to the folder to download subtitles in

optional arguments:
  -h, --help            show this help message and exit
  --language language, -l language
                        The language to download the subtitles in
```
