1. Edit `description.csv` to specify what prompts to generate images for and how many requests to send (4 images per request), set `num_generated` column to 0 at first.
2. Change the API in `generate_textures.py` to your own, the API website is https://dashboard.goapi.ai
3. Run `generate_textures.py`, this sends all requests for generation.
4. Wait for image generation to complete, wait up to a couple hours (otherwise the tasks expire in Midjourney), then run `upscale_textures.py`, which upscales each of the four images per request.
5. After those upscales complete, run `fetch_results.py` to download the upscaled images.
