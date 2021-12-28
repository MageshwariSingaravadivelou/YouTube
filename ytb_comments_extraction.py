import os
import pandas as pd
import googleapiclient.discovery

videoIds= ["v73TaVDWh4s", "0-TEzySiNv8", "ATIVwXhTXHg", "--CIF7dIVl8", "LTbmEA0nEyc"]

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "YOUR DEVELOPER KEY" 

def pagination(video_id, nextPage = None):
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
    if nextPage == None:
        request = youtube.commentThreads().list(
        part="replies,snippet",
        maxResults = 100,
        videoId=video_id
        )

    else:
        request = youtube.commentThreads().list(
        part="replies,snippet",
        pageToken = nextPage,
        maxResults = 100,
        videoId=video_id
        )

    response = request.execute()

    return response


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    main_df = pd.DataFrame()
    for each in videoIds:
        print("Video Id: {}".format(each))
        response = pagination(video_id=each)
        while True:
            df = pd.DataFrame(response["items"])
            main_df = main_df.append(df)
            main_df.to_csv(r"ytb_comments.csv", index=False)
            try:
                print(response["nextPageToken"])
                response = pagination(video_id=each, nextPage=response["nextPageToken"])
            except KeyError:
                main_df = main_df.append(pd.DataFrame(response["items"]))
                main_df.to_csv(r"ytb_comments.csv", index=False)
                break
    

if __name__ == "__main__":
    main()
