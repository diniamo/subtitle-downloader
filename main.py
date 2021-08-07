from dotenv import load_dotenv
from argparse import ArgumentParser
from os import path, getenv
import glob
from tqdm import tqdm

from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File


EXTENSIONS = [
    'mp4',
    'mkv',
    'avi'
]

load_dotenv(path.join(path.dirname(path.realpath(__file__)), '.env'))
ost = OpenSubtitles()
ost.login(getenv('L_USERNAME', ''), getenv('L_PASSWORD', ''))

with open("available_languages.txt", 'r') as f:
    LANGUAGES = f.read().splitlines()


def dir_path(string):
    if path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def parse_args():
    parser = ArgumentParser(
        description="Download subtitles from opensubtitles.org, for every video file found in the specified directory."
    )
    parser.add_argument('path', type=dir_path, help="The path to the folder to download subtitles in")
    parser.add_argument('--language', '-l',
                        type=str,
                        help="The language to download the subtitles in",
                        choices=LANGUAGES,
                        default='eng',
                        metavar='language')

    args = parser.parse_args()
    return args.path, args.language


def get_video_files(f_path):
    print("Searching for video files...")
    a_path = path.join(f_path, '**/*.')

    c_files = []
    for ext in EXTENSIONS:
        c_files.append(glob.glob(a_path + ext, recursive=True))

    # Flattens list
    flat = [item for sublist in c_files for item in sublist]
    print(f"Found {len(flat)} video files")
    return flat


def download_subtitles(i_files, lang):
    for file in tqdm(i_files, 'Downloading', unit_scale=True):
        fu = File(file)
        data = ost.search_subtitles([{
            'sublanguageid': lang,
            'moviehash': fu.get_hash(),
            'moviebytesize': fu.size
        }])

        if len(data) == 0:
            print("No subtitles found")
            exit()
        id_subtitle_file = data[0].get('IDSubtitleFile')

        ost.download_subtitles(
            [id_subtitle_file],
            {id_subtitle_file: file.rsplit('.', 1)[0]+'.srt'},
            output_directory=path.dirname(file),
            extension='srt'
        )


if __name__ == '__main__':
    args = parse_args()
    files = get_video_files(args[0])

    if len(files) == 0:
        exit(-1)

    download_subtitles(files, args[1])

