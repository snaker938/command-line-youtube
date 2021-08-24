"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import textwrap
from typing import Sequence
import random



class VideoPlayer:

    """A class used to represent a Video Player."""
    def __init__(self):
        self._video_library = VideoLibrary()
        self._currentVideo = None
        self._isPaused = False
        self._playlists = {}


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = []
        flagString = ""
        for x in self._video_library.get_all_videos():
            if x._flag:
                flagString = f"- FLAGGED (reason: {x._flag})"

            video = f"  {x.title} ({x.video_id}) [{x.tags_finale}] {flagString}"
            videos.append(video)

        videosSorted = sorted(videos)
        i = 0
        for x in self._video_library.get_all_videos():
            print(videosSorted[i])
            i = i + 1

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        videosId = []
        videosName = []
        for x in self._video_library.get_all_videos():
            videoId = f"{x.video_id}"
            videosId.append(videoId)
            videoName = f"{x.title}"
            videosName.append(videoName)
        i = 0
        foundVideo = False
        for x in self._video_library.get_all_videos():
            if video_id == videosId[i]:
                foundVideo = True
                foundVideoName = videosName[i]
            elif not foundVideo:
                foundVideo = False
            i = i + 1
        
        if not foundVideo:
            print("Cannot play video: Video does not exist")
            return
        
        if video._flag:
            print(f"Cannot play video: Video is currently flagged (reason: {video._flag})")
            return

        if self._currentVideo:
          self.stop_video()
        print(f"Playing video: {foundVideoName}")
        self._currentVideo = video

    def stop_video(self):
        """Stops the current video."""
        if self._currentVideo is None:
            print("Cannot stop video: No video is currently playing")
            return
        
        print(f"Stopping video: {self._currentVideo.title}")
        self._currentVideo = None
        self._isPaused = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        videosId = []
        videosName = []
        for x in self._video_library.get_all_videos():
            videoId = f"{x.video_id}"
            videosId.append(videoId)
            videoName = f"{x.title}"
            videosName.append(videoName)
        
        num_videos = len(self._video_library.get_all_videos()) - 1



        randomVideoIndex = random.randint(0,num_videos)
        randomVideoId = videosId[randomVideoIndex]

        video = self._video_library.get_video(randomVideoId)

        numFlag = 0

        for x in self._video_library.get_all_videos():
            video = self._video_library.get_video(x.video_id)
            if video._flag:
                numFlag = numFlag + 1

        if numFlag > num_videos:
            print("No videos available")
            return
        
        video = self._video_library.get_video(randomVideoId)


        while video._flag:
            videosId = []
            videosName = []
            for x in self._video_library.get_all_videos():
                videoId = f"{x.video_id}"
                videosId.append(videoId)
                videoName = f"{x.title}"
                videosName.append(videoName)
            
            num_videos = len(self._video_library.get_all_videos()) - 1
            randomVideoIndex = random.randint(0,num_videos)
            randomVideoId = videosId[randomVideoIndex]

            video = self._video_library.get_video(randomVideoId)

        self.play_video(randomVideoId)
        


    def pause_video(self):
        """Pauses the current video."""
        if self._currentVideo is None:
            print("Cannot pause video: No video is currently playing")
            return
        if self._isPaused:
            print(f"Video already paused: {self._currentVideo.title}")
        else:
            print(f"Pausing video: {self._currentVideo.title}")
            self._isPaused = True


    def continue_video(self):
        """Resumes playing the current video."""
        if self._currentVideo is None:
            print("Cannot continue video: No video is currently playing")
        elif self._isPaused:
            print(f"Continuing video: {self._currentVideo.title}")
            self._isPaused = False
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self._isPaused:
            videoStatus = "- PAUSED"
        else:
            videoStatus = ""
        if self._currentVideo is None:
            print("No video is currently playing")
            return
        video = f"{self._currentVideo.title} ({self._currentVideo.video_id}) [{self._currentVideo.tags_finale}]"
        print(f"Currently playing: {video} {videoStatus}")
        

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowerPlaylistName = playlist_name.lower()
        if lowerPlaylistName in self._playlists:
          print("Cannot create playlist: A playlist with the same name already exists")
          return
        print(f"Successfully created new playlist: {playlist_name}")
        self._playlists[lowerPlaylistName] = Playlist(playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        videosId = []
        videosName = []

        video = self._video_library.get_video(video_id)

        for x in self._video_library.get_all_videos():
            videoId = f"{x.video_id}"
            videosId.append(videoId)
            videoName = f"{x.title}"
            videosName.append(videoName)
        i = 0
        foundVideo = False
        lowerPlaylistName = playlist_name.lower()
        for x in self._video_library.get_all_videos():
            if video_id == videosId[i]:
                foundVideo = True
                foundVideoName = videosName[i]
                foundVideoId = videosId[i]
            elif not foundVideo:
                foundVideo = False
            i = i + 1
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[lowerPlaylistName]
        if not foundVideo:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif video._flag:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video._flag})")
            return
        elif foundVideoId in playlist.videos:
            print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            playlist.videos.append(foundVideoId)
            print(f"    Added video to {playlist_name}: {foundVideoName}")       


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print("No playlists exist yet")
        else:
            print(f"Showing all playlists:")
            
            playlists = self._playlists
            playlistsSorted = sorted(playlists)
            i = 0            
            for playlist in playlistsSorted:
                print(f"    {playlists[playlist].name} {self.num_videos_in_playlist(playlistsSorted[i])}")
                i = i + 1
          
    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        if not playlist.videos:
            print(f"Showing playlist: {playlist_name}")
            print(f"    No videos here yet")
            return
        else:
            flagString = ""
            print(f"Showing playlist: {playlist_name}")
            for video in playlist.videos:
                video = self._video_library.get_video(video)
                if video._flag:
                    flagString = f"- FLAGGED (reason: {video._flag})"
                videoPrint = f"{video.title} ({video.video_id}) [{video.tags_finale}] {flagString}"
                print(f"    {videoPrint}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        videosInPlaylist = []
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        videosId = []
        videosName = []
        for x in self._video_library.get_all_videos():
            videoId = f"{x.video_id}"
            videosId.append(videoId)
            videoName = f"{x.title}"
            videosName.append(videoName)
        i = 0
        foundVideo = False
        videoInPlaylist = False
        lowerPlaylistName = playlist_name.lower()
        for x in self._video_library.get_all_videos():
            if video_id == videosId[i]:
                foundVideo = True
                foundVideoName = videosName[i]
                foundVideoId = videosId[i]
                foundVideoIndex = i
            elif not foundVideo:
                foundVideo = False
            i = i + 1
        if not foundVideo:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return
        
        for video in playlist.videos:
            videoExtra = self._video_library.get_video(video)
            self._currentVideo = videoExtra
            videoId = self._currentVideo.video_id
            videosInPlaylist.append(videoId)
        
        num_videos = len(self._video_library.get_all_videos())
      
        

        leftOver = num_videos - videosInPlaylist.__len__()
        for x in range (0, leftOver):
            videosInPlaylist.append(None)

        for x in range (0, num_videos):
            if videosInPlaylist[x] == videoId:
                videoInPlaylist = True
        
        if not videoInPlaylist:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return

        if videoInPlaylist:
            playlist.videos.remove(foundVideoId)
            print(f"Removed video from {playlist_name}: {foundVideoName}")

       
    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return
        
        playlist = self._playlists[playlist_name.lower()]
        if not playlist.videos:
            print(f"Cannot clear playlist {playlist_name}: There are no videos to clear")
            return
        else:
            playlist.videos.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() not in self._playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return
        playlist = self._playlists[playlist_name.lower()]
        playlist.videos.clear()
        print(f"Deleted playlist: {playlist_name}")
        del self._playlists[playlist_name]
        

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = []
        videosFound = []
        videosId = []
        

        
        
        for video in self._video_library.get_all_videos():
            if search_term.casefold() in video.title.casefold() and not video._flag:
                videos.append(video)

        
        if not videos:
            print(f"No search results for {search_term}")
            return
        videosFound = sorted(videos, key=lambda x: x.title)
    
       
       

        
        print(f"Here are the results for {search_term}:")
        if not videosFound:
            print(f"No search results for {search_term}")
            return
      

        for i, x in enumerate(videosFound):
            print(f"    {i + 1}) {x.title} ({x.video_id}) [{x.tags_finale}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        

        while True:
            try:
                videoNum = int(input())
                if isinstance(videoNum, int):
                    break
            except ValueError:
                return


        if not videoNum:
            return

        
        videoNum = int(videoNum)
        videoNum = videoNum - 1
        numVideosInSearch = len(videosFound) - 1
        if videoNum > numVideosInSearch or videoNum < 0:
            return
        else:
            i = 0
            self.play_video(videosFound[videoNum].video_id)






    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        videos = []
        videosFound = []
        videosId = []
      



        

    
        i = 0

        for video in self._video_library.get_all_videos():
            if video_tag.casefold() in video.tags and not video._flag:
                videos.append(video)
            i = i + 1


        
        if not videos:
            print(f"No search results for {video_tag}")
            return
        videosFound = sorted(videos, key=lambda x: x.title)
    
       
       

        
        print(f"Here are the results for {video_tag}:")
        if not videosFound:
            print(f"No search results for {video_tag}")
            return
      

        for i, x in enumerate(videosFound):
            print(f"    {i + 1}) {x.title} ({x.video_id}) [{x.tags_finale}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        

        while True:
            try:
                videoNum = int(input())
                if isinstance(videoNum, int):
                    break
            except ValueError:
                return


        if not videoNum:
            return

        
        videoNum = int(videoNum)
        videoNum = videoNum - 1
        numVideosInSearch = len(videosFound) - 1
        if videoNum > numVideosInSearch or videoNum < 0:
            return
        else:
            i = 0
            self.play_video(videosFound[videoNum].video_id)    
        
     



    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        if not flag_reason:
            flagReason = "Not supplied"
        else:
            flagReason = flag_reason


        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot flag video: Video does not exist")
            return
        
        if video._flag:
            print("Cannot flag video: Video is already flagged")
            return

        video.setFlag(flagReason)

        if video == self._currentVideo:
            self.stop_video()

        if video == self._currentVideo:
            if self._isPaused:
                self.stop_video()

        print(f"Successfully flagged video: {video.title} (reason: {flagReason})")




    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
    

        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot remove flag from video: Video does not exist")
            return
        
        if not video._flag:
            print("Cannot remove flag from video: Video is not flagged")
            return

        video.setFlag(None)

        print(f"Successfully removed flag from video: {video.title}")


    def num_videos_in_playlist(self, playlist_name):
        numFlag = 0
        numNormal = 0
        playlist = self._playlists[playlist_name.lower()]
        for video in playlist.videos:
                video = self._video_library.get_video(video)
                if video._flag:
                    numFlag = numFlag + 1
                else:
                    numNormal = numNormal + 1

        if numNormal == 1 and numFlag == 1:
            return f"({numNormal} normal video, {numFlag} flagged video)"
        
        elif numNormal == 1:
            return f"({numNormal} normal video, {numFlag} flagged videos)"

        elif numFlag == 1:
            return f"({numNormal} normal videos, {numFlag} flagged video)"
        
        elif numFlag == 0:
            return f"({numNormal} normal videos)"

        else:
            return f"({numNormal} normal videos, {numFlag} flagged videos)"


    def create_video(self, video_title, video_id, video_tags):

        videoTitle = video_title
        videoTitle = videoTitle.replace("-", " ")
        


        videos = []
        for x in self._video_library.get_all_videos():
            video = x.title
            videos.append(video)
        i = 0

        if videoTitle in videos:
            print("Cannot create video: video_title is already used!")
            return
        



        video = self._video_library.get_video(video_id)
        if video is not None:
            print("Cannot create video: video_id is already used!")
            return

    


        videoTags = []
        videoTagsNonArray = video_tags

        videoTagsNonArray = videoTagsNonArray.replace(",", " ")

        videoTags = videoTagsNonArray.split(" ")

        listVideoTitle = list(videoTitle)
        listVideoTitle[0] = videoTitle[0].capitalize()
        videoTitle = "".join(listVideoTitle) 



        if "[]" in videoTags:
            videoTags = []
            newVideoConfirmPrint = f"Your new video will have a title: {videoTitle} | a video id of: {video_id} | and will have no tags"
        else:
            videoTags = ["#" + videoTags for videoTags in videoTags]

            newVideoConfirmPrint = f"Your new video will have a title: {videoTitle} | a video id of: {video_id} | and will have tags consiting of {videoTags}."

        

        
        newVideoTemp = f"{videoTitle} {video_id} {videoTags}"

       

        print(newVideoConfirmPrint)
        print(" ")
        print("Are these inputs correct?")
        print(" ")

        while True:
            a = input("Enter yes/no to continue: ")
            if a.lower()=="yes":
                break
            elif a.lower()=="no":
                return
            else:
                print("Enter either yes/no")

        
        videoTitle = videoTitle.replace(" ", "-")

        if not videoTags:
            self._video_library.add_video(videoTitle, video_id, "")
            return
        else:
            self._video_library.add_video(videoTitle, video_id, videoTags)

    
    
    def delete_video(self):
        self._video_library.delete_video()

            
        








    





 