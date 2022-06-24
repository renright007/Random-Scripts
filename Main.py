from YoutubeStats import YTstats

API_KEY = 'AIzaSyAI5no8arQNT5ZSJmxFGlSoFd52E7fcPDg'
channel_id = "UC160Ln3rSb3Ym2iUxJasZVw"

yt = YTstats(API_KEY, channel_id)
#yt.get_channel_stats()
#yt.dump()
yt.get_channel_video_data()