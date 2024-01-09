import requests
import os
import time


API_KEY = "32bb99d9413fdbaac5f1195b5dd087ffef9d38443523d67588a119af284fcd33"
headers = {"X-API-KEY": API_KEY}
endpoint = "https://api.midjourneyapi.xyz/mj/v2/upscale"

for name in os.listdir("textures"):
    if name.startswith('.'):
        continue
    print("Upscaling images for textures: \"{}\"".format(name))

    name_path = os.path.join("textures", name)
    # image_path = os.path.join(name_path, "upscaled_images")
    # os.makedirs(image_path, exist_ok=True)

    task_ids = open(os.path.join(name_path, "task_ids.txt"), 'r')
    print("reading ids from:", os.path.join(name_path, "task_ids.txt"))

    try:
        upscale_task_ids = open(os.path.join(name_path, "upscale_task_ids.txt"), 'r')
        upscaled = [s.strip() for s in upscale_task_ids.readlines()]
        upscale_task_ids.close()
    except:
        upscaled = list()
    upscale_task_ids = open(os.path.join(name_path, "upscale_task_ids.txt"), 'a')

    remaining_ids = list()
    for id in task_ids.readlines():
        id = id.strip()
        if id in upscaled:
            continue

        # upscale all four images
        new_ids = list()
        for i in range(1, 5):
            data = {
                "origin_task_id": id,
                "index": str(i),
                "webhook_endpoint": "",
                "webhook_secret": "",
                "mode": "fast"
            }
            response = requests.post(endpoint, headers=headers, json=data)
            print("\tSent request #{}, status: {}".format(i, response.status_code))

            # check that request is successful
            if response.status_code != 200:
                print("\nError sending request:\n", response.json())
                break
            # store task id and metadata
            new_ids.append(response.json()["task_id"] + '\n')

        # write all or not at all
        if len(new_ids) == 4:
            for id in new_ids:
                upscale_task_ids.write(id)
        else:
            remaining_ids.append(id)
            print("\tNot all requests sent, aborting all four")
        
    task_ids.close()
    upscale_task_ids.close()
    print()

    # write remaining ids back, avoids repeated requests
    with open(os.path.join(name_path, "task_ids.txt"), 'w') as f:
        f.write('\n'.join(remaining_ids) + '\n')
