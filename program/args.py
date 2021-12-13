import argparse

def get_args(video_path='../data/video/Shortcake_SONG_shorts_1080pFHR.mp4',
             start_over=False,
             with_audio=True,
             alpha=1.2,
             beta=0.0):
    """
    Get command line arguments.
    Arguments set the default values of command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path", "-v", type=str, default=video_path)
    parser.add_argument("--start-over", "-s", action="store_true", default=start_over)
    parser.add_argument("--with_audio", "-a", action="store_true", default=with_audio)
    parser.add_argument("--alpha", type=float, default=alpha)
    parser.add_argument("--beta", type=float, default=beta)

    return parser.parse_args()
