import urllib.request 
from PIL import Image 

# Retrieving the resource located at the URL 
# and storing it in the file name a.png 
url = "https://media.geeksforgeeks.org/wp-content/uploads/20210224040124/JSBinCollaborativeJavaScriptDebugging6-300x160.png" 
urllib.request.urlretrieve(url, "geeksforgeeks.png") 

# Opening the image and displaying it (to confirm its presence) 
img = Image.open(r"geeksforgeeks.png") 
img.show()
