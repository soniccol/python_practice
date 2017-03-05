#encoding: UTF-8

import os
import pymysql.cursors
import youtube_dl
import subprocess, sys
from subprocess import call
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    part="snippet",
    channelId="",
    type="video",
    videoDuration="long",
    order="date",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []
  
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s,%s" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s,%s" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s,%s" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  print "Videos:", "\n".join(videos)
  return videos;
#  print "Channels:\n", "\n".join(channels), "\n"
#  print "Playlists:\n", "\n".join(playlists), "\n"


def insertIntoDB(link):
# Connect to the database
  connection = pymysql.connect(host='localhost',user='',password='',db='',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

  linkData= link[0].split(',')
  print linkData[0]
  print linkData[1]
  
  print "Check if the id is existed in the db."

  ydl_opts = {
    'verbose': True,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


  try:
    with connection.cursor() as cursor:
      # Read a single record
      sql = "SELECT count(*) as c from mrplayer  WHERE videoId=%s"
      cursor.execute(sql, (linkData[1],))
      result = cursor.fetchone()
#      print type(result["c"])
      if result["c"]==0:
          with connection.cursor() as cursor:
            sql = "INSERT INTO mrplayer (videoTitle, videoId) VALUES (%s, %s)"
            cursor.execute(sql, (linkData[0], linkData[1]))
          connection.commit()
          cmd = 'youtube-dl -f 137+140/mp4+mp3 https://www.youtube.com/watch?v='+linkData[1]
          retcode = subprocess.call(cmd, shell=True)
      else:
          print "The video is already existed."
          cmd = 'youtube-dl -f 137+140/mp4+mp3 https://www.youtube.com/watch?v='+linkData[1]
          retcode = subprocess.call(cmd, shell=True)
  finally:
    connection.close()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=1)
  args = argparser.parse_args()

  videoLink=[]

  try:
    videoLink=youtube_search(args)
    insertIntoDB(videoLink)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
