import requests
import json
import os

URL = "https://gql-realtime-2.reddit.com/query"
BEGINNING = 1648817027221
END = 1649112460185
# Including whites
# END = 1649116967221

PAYLOAD = {
    "operationName": "frameHistory",
    "variables": {
        "input": {
            "actionName": "get_frame_history",
            "GetFrameHistoryMessageData": {
                "timestamp": 1649112460185}}},
    "query": "mutation frameHistory($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetFrameHistoryResponseMessageData {\n            frames {\n              canvasIndex\n              url\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

frames = []
for i, timestamp in enumerate(range(BEGINNING, END, 60000)):
    PAYLOAD["variables"]["input"]["GetFrameHistoryMessageData"]["timestamp"] = timestamp
    # for downloading the last official frame
    # for i in range(1):
    # PAYLOAD["variables"]["input"]["GetFrameHistoryMessageData"]["timestamp"] = 1649112460185
    payload = PAYLOAD
    print(payload)
    r = requests.post(URL, json=payload, headers={'Authorization': 'Bearer -fNRQAKYVqdPxfQVNCm4F4X4asU_d6A',
                                                  "Content-Type": "application/json"})
    print(r.text)
    if r.ok:
        base_path = os.path.join("frames", str(1649112460185))
        os.makedirs(base_path, exist_ok=True)
        for frame in r.json()["data"]["act"]["data"][0]["data"]["frames"]:
            file_name = f"{frame['canvasIndex']}.png"
            destination = os.path.join(base_path, file_name)
            if not os.path.exists(destination):
                print(f"Fetching {destination}")
                img = requests.get(frame["url"]).content
                with open(destination, "wb") as f:
                    f.write(img)
