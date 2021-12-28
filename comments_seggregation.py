# DEVELOPER_KEY = "AIzaSyBOVKDx52ojkOqLkn7E8KsLkrSw-ZieKwc"
import os
import pandas as pd
import googleapiclient.discovery

videoIds= ["v73TaVDWh4s", "0-TEzySiNv8", "ATIVwXhTXHg", "--CIF7dIVl8", "LTbmEA0nEyc"]

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyBM16YUknYgpcsp1JgFWdaY9S73Mxzefdc"

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
    main_comments = []
    for id in videoIds:
        print("Video Id: {}".format(id))
        response = pagination(video_id=id)

        while True:
            for each in response["items"]:
                main_comments.append(each["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            try:
                print(response["nextPageToken"])
                response = pagination(video_id=id, nextPage=response["nextPageToken"])
            except KeyError:
                for each in response["items"]:
                    main_comments.append(each["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                break
    main_df = pd.DataFrame(main_comments)
    main_df.to_csv(r"C:/Users/v-msingarava/Desktop/edge_features_comments.csv", index=False)

if __name__ == "__main__":
    main()