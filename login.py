import logging
from apiclient.discovery import build

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
  service = build('youtube', 'v3', developerKey='')
  print service.search().list(
      port='snippet',
      channelId=''
    ).execute()

if __name__ == '__main__':
  main()
