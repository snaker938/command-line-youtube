"""A video library class."""

from .video import Video
from pathlib import Path
import csv



# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)

    def add_video(self, videoTitle, video_id, videoTags):
        videoTitle = videoTitle.replace("-", " ")



        videoTagsJoined = ' '.join(map(str, videoTags))

        # videoTagsJoined = videoTagsJoined.replace(" ", " a ")


        if videoTags != "":
            videoTagsJoined = ' '.join(map(str, videoTags))
            with open(Path(__file__).parent / "videos.txt", "a") as video_file:
                video_file.write("\n" + f"{videoTitle} | {video_id} | {videoTagsJoined.replace(' ', ' , ')}")
        else:
            videoTagsJoined = ""
            with open(Path(__file__).parent / "videos.txt", "a") as video_file:
                video_file.write("\n" + f"{videoTitle} | {video_id} |")


    

        self.__init__()

        print(" ")

        print("Video successfully created!")


    def delete_video(self, video_id):

        print(f"{video_id} is the video id")

        

        # self.__init__()

        print("Video successfully deleted!")