import requests
import time
import os


endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"


def download_images(image_path, ids_file_path, remove_downloaded=True):
    remaining_ids = list()
    with open(ids_file_path, 'r') as f:
        ids = f.readlines()

    for id in ids:
        id = id.strip()
        if not id:
            continue
        
        if os.path.exists(image_path) and id + ".png" in os.listdir(image_path):
            # image already downloaded
            continue
        print("\tRetrieving image for task_id:", id)

        # retrieve image url
        data = {"task_id": id}
        response = requests.post(endpoint, json=data)
        # print(response.json())
        image_url = response.json()["task_result"]["image_url"]

        # check if image generation is complete
        if not image_url:
            print("\tImage generation not yet complete")
            remaining_ids.append(id)
            continue

        # download image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            # create folder for images if necessary
            os.makedirs(image_path, exist_ok=True)
            with open(os.path.join(image_path, id + ".png"), 'wb') as f:
                f.write(response.content)
        else:
            print("\tImage download failed with status:", response.status_code)
            break
    
    if remove_downloaded:
        # write undownloaded images
        with open(ids_file_path, 'w') as f:
            f.write('\n'.join(remaining_ids) + '\n')


# keep fetching results as they come in
while True:
    for name in os.listdir("textures"):
        if name.startswith('.'):
            continue
        print("Downloading images for name: \"{}\"".format(name))

        name_path = os.path.join("textures", name)
        image_path = os.path.join(name_path, "images")

        task_ids_path = os.path.join(name_path, "task_ids.txt")
        upscale_task_ids_path = os.path.join(name_path, "upscale_task_ids.txt")

        # todo: close files
        download_images(
            os.path.join(name_path, "images"),
            task_ids_path,
            remove_downloaded=False
        )
        
        # download upscaled images
        if os.path.exists(upscale_task_ids_path):
            download_images(
                os.path.join(name_path, "upscaled_images"),
                upscale_task_ids_path
            )

        print()

    print("Waiting before retrying download")
    time.sleep(5)
    print()
