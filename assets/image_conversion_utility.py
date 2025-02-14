from PIL import Image
import os

def png_to_ico(png_path, ico_path):
    # Open the PNG image
    image = Image.open(png_path)
    
    # Save the image as an ICO file
    image.save(ico_path, format='ICO')

# Example usage
# png_to_ico("favicon.png", "favicon.ico")

def all_to_webp(input_dir = "./", output_dir = "./as_webp/"):

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Supported image formats for conversion
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

    # Convert images to WebP
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(image_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".webp")

            with Image.open(input_path) as img:
                img.save(output_path, "WEBP", quality=80)  # Adjust quality as needed
                print(f"Converted: {filename} → {output_path}")
                
# Example usage
all_to_webp()