import glob
from argparse import ArgumentParser
from os import getenv, makedirs
from shutil import move

from dotenv import load_dotenv
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from tqdm import tqdm

from utils import *

EXTENSIONS = [
    'mp4',
    'mkv',
    'avi'
]

load_dotenv(path.join(getcwd(), '.env'))
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

    r_args = parser.parse_args()
    return r_args.path, r_args.language


def get_video_files(f_path):
    print("Searching for video files...")
    a_path = path.join(f_path, '**/*.')

    c_files = []
    for ext in EXTENSIONS:
        c_files.append(glob.glob(a_path + ext, recursive=True))

    # Flattens list
    flat = flatten(c_files)
    print(f"Found {len(flat)} video files")
    return flat


def download_subtitles(i_files, lang):
    id_l = []
    d_dict = {}
    for file in tqdm(i_files, 'Querying'):
        fu = File(file)
        data = ost.search_subtitles([{
            'sublanguageid': lang,
            'moviehash': fu.get_hash(),
            'moviebytesize': fu.size
        }])

        if len(data) == 0:
            print("No subtitles found")
            exit(-1)

        id_subtitle_file = data[0].get('IDSubtitleFile')
        id_l.append(id_subtitle_file)
        d_dict[id_subtitle_file] = path.join(path.dirname(file), path.basename(file).rsplit('.', 1)[0] + '.srt')

    tmp = path.join(getcwd(), "tmp")
    if not path.isdir(tmp):
        makedirs(tmp)

    id_l_e = [s + '.srt' for s in id_l]

    id_l_new = chunks(id_l, 20)
    id_l_e_new = chunks(id_l_e, 20)
    for il, ile in tqdm(zip(id_l_new, id_l_e_new), 'Downloading chunks'):
        ost.download_subtitles(
            il,
            dict(zip(il, ile)),  # We pair the subtitle IDs to (themselves + '.srt')
            output_directory=tmp,
            extension='srt'
        )

    for fp, s_id in zip([path.join(tmp, x) for x in id_l_e], id_l):
        move(fp, d_dict[s_id])


if __name__ == '__main__':
    cleanup()

    args = parse_args()
    files = get_video_files(args[0])

    if len(files) == 0:
        exit(-1)

    download_subtitles(files, args[1])

    cleanup()

