from PIL import Image
import os

# Add files or patterns to skip here
SKIP_FILES = [
    'desktools',     # Will skip any file with 'skip' in the name
    'logo', # Will skip any file with 'original' in the name
    'MOBtools'
    # Add more keywords as needed
]

def should_skip_file(filename):
    """
    Check if the file should be skipped based on its name.
    Returns True if the file should be skipped.
    """
    return any(skip_word.lower() in filename.lower() for skip_word in SKIP_FILES)

def convert_to_white():
    """
    Converts all non-transparent pixels to white in PNG and WEBP images while preserving transparency.
    Processes images in the same directory as the script, excluding files with specified keywords.
    """
    # Get the directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Supported file extensions
    supported_formats = {'.png', '.webp'}
    
    # Iterate through all files in the current directory
    for filename in os.listdir(current_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        
        # Skip files that match the skip patterns
        if should_skip_file(filename):
            print(f"Skipping: {filename}")
            continue
            
        # Check if file is a supported image format
        if file_ext in supported_formats:
            input_path = os.path.join(current_dir, filename)
            
            try:
                # Open the image
                with Image.open(input_path) as img:
                    # Convert to RGBA if not already
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # Get image data as a list of pixels
                    data = img.getdata()
                    
                    # Create new image data
                    new_data = []
                    for item in data:
                        # If pixel is not fully transparent
                        if item[3] != 0:
                            # Make it white while preserving original alpha
                            new_data.append((255, 255, 255, item[3]))
                        else:
                            # Keep fully transparent pixels as is
                            new_data.append(item)
                    
                    # Create new image with modified data
                    img.putdata(new_data)
                    
                    # Save the modified image, overwriting the original
                    img.save(input_path, format=img.format)
                    print(f"Processed: {filename}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    convert_to_white()
    print("Processing complete!")