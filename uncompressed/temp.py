from PIL import Image

#conda create -n temp
#conda activate temp
#conda install pillow -y

def png_to_ico(png_path, ico_path):
    # Open the PNG image
    image = Image.open(png_path)
    
    # Save the image as an ICO file
    image.save(ico_path, format='ICO')

png_to_ico("favicon.png", "favicon.ico")
# python temp.py
# conda deactivate
# conda env remove -n temp