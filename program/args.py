import argparse

def get_args(video_path='../data/video/Shortcake_SONG_shorts_1080pFHR.mp4'):
    """
    Get command line arguments.
    Arguments set the default values of command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path", "-m", type=str, default=video_path)

    return parser.parse_args()
