from PIL import Image

def png_to_ico(png_path, ico_path):
    # Open the PNG image
    image = Image.open(png_path)
    
    # Save the image as an ICO file
    image.save(ico_path, format='ICO')

# Example usage
png_to_ico("favicon.png", "favicon.ico")
