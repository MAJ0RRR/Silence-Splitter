from natsort import natsorted
from file_splitter import FileSpliter
import os
import pydub
import tempfile
import argparse

def join_audio(input, output):
    slices = [f for f in os.listdir(input) if f.endswith('.wav')]
    slices = natsorted(slices)
    audio_segments = []  

    for s in slices:
        path = os.path.join(input, s)
        audio_segment = pydub.AudioSegment.from_file(path)
        audio_segments.append(audio_segment)

    joined_audio = pydub.AudioSegment.empty()
    for s in audio_segments:
        joined_audio = joined_audio + s

    joined_audio.export(output, format="mp3")
    
    
def split_silence(destination, source, silence_threshs, min_silence_lens):
    tempdir = tempfile.TemporaryDirectory()

    if os.path.exists(f"{destination}/*"):
        os.system(f"rm {destination}/*")

    # Convert to .wav
    os.system(f"find {source} -name '*.mp3' -exec bash -c 'for f; \
              do ffmpeg -i \"$f\" -acodec pcm_s16le -ar 22050 \
              -ac 1 \"{tempdir.name}/$(basename -s .mp3 $f)\".wav \
              -loglevel error; done' _ {{}} +")
    os.system(f"find {source} -name '*.wav' -exec bash -c 'for f; \
              do ffmpeg -y -i \"$f\" -acodec pcm_s16le -ar 22050 \
              -ac 1 \"{tempdir.name}/$(basename -s .wav $f)\".wav \
              -loglevel error; done' _ {{}} +")

    fileSpliter = FileSpliter(f"{tempdir.name}/*.wav", f"{destination}")
    fileSpliter.split_silence(silence_threshs, min_silence_lens)

    tempdir.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog = 'splits_silence',
    description = 'Splits wav files into chunks on silence.'
    )
    parser.add_argument('-t', '--thresholds', action='store', dest='silence_threshs', nargs="*", type=int,
        default=[-45], help='Thresholds below which audio is considered silent. Default: [-45].')
    parser.add_argument('-l', '--lengths-silence', action='store', dest='min_silence_lens', nargs="*", type=int,
        default=[300], help='Lengths of silence in miliseconds on which splitting happens. Default: [300].')
    parser.add_argument('-s', '--source', action='store', dest='source', type=str,
        default='input', help='')
    parser.add_argument('-d', '--destiantion', action='store', dest='destination', type=str,
        default='output', help='')
	
    parsed = parser.parse_args()
	
    if len(parsed.silence_threshs) != len(parsed.min_silence_lens):
        print("List of --thresholds has to have same number of elements as --lengths-silence!")
        exit(1)

    split_silence(parsed.destination, parsed.source, parsed.silence_threshs, parsed.min_silence_lens)
    join_audio(parsed.destination, "joined/joined.mp3")