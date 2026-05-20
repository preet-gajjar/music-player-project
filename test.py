import coverpy
import requests 
from PIL import Image

# Instance CoverPy
c = coverpy.CoverPy()
music_Name = input('Enter the name of Song: ')
try:
	result = c.get_cover(music_Name)
	# Set a size for the artwork (first parameter) and get the result url.
	url=result.artwork(625)  
except coverpy.exceptions.NoResultsException as e:
	url="https://styles.redditmedia.com/t5_33hhf/styles/communityIcon_w8oddhw38pn51.png"
	music_Name='Not Found'


data = requests.get(url).content

f = open(f'/Users/manit/Documents2/musicplayer-main/Cover_Albums/{music_Name}.jpg','wb') 

f.write(data) 
f.close()
