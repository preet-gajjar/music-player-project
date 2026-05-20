import requests
import coverpy

def album_cover(image_current_path):
    c = coverpy.CoverPy()
    try:
        result = c.get_cover(image_current_path)
        url = result.artwork(170)
    except coverpy.exceptions.NoResultsException as e:
        result = c.get_cover("SolarJH")
        url = result.artwork(170)
    data = requests.get(url).content

    f = open(f'/Users/manit/Documents2/musicplayer-main/Cover_Albums/{image_current_path}.jpg','wb') 

    f.write(data)
    f.close()