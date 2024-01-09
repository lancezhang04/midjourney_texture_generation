import requests
import pandas as pd
import os


# configurations for third-party API
API_KEY = "32bb99d9413fdbaac5f1195b5dd087ffef9d38443523d67588a119af284fcd33"
endpoint = "https://api.midjourneyapi.xyz/mj/v2/imagine"
headers = {"X-API-KEY": API_KEY}

# csv that stores information on what to generate
df = pd.read_table("descriptions.csv", sep=',')

for r_idx, r in df.iterrows():
    generated = int(r["num_generated"])
    num_gen = int(r["num_target"])
    to_generate = num_gen - generated
    if to_generate <= 0:
        continue
    
    description = r["description"]
    print("Generating images for description: \"{}\"".format(description))
    data = {
        "prompt": "{}, texture image, high ".format(description) +
                  "quality, 8k, photorealistic --tile",
        "process_mode": "fast"  # about 5 cents per prompt
    }
    print("Prompt:", data["prompt"])

    # create corresponding folders
    os.makedirs("textures/{}".format(description), exist_ok=True)
    task_ids = open("textures/{}/task_ids.txt".format(description), 'a')

    for i in range(to_generate):
        response = requests.post(endpoint, headers=headers, json=data)
        print("\tSent request #{}, status: {}".format(i + 1, response.status_code))

        # check that request is successful
        if response.status_code != 200:
            print("\nError sending request:\n", response.json())
            break
        # store task id and metadata
        task_ids.write(response.json()["task_id"] + '\n')
        df.at[r_idx, "num_generated"] = generated + i + 1
        
    task_ids.close()
    print()

df.to_csv("descriptions.csv", index=False)
