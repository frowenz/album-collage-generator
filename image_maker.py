import os 
from PIL import Image, ImageStat
import random
import sys
import colorsys

# WARNING:
# This is a destructive process –– you should back up your images before running this script.

# Removes images that are not square 
# Most spotify albums are 640 x 640
def filter_images_by_size(folder):
    for file_name in os.listdir(folder):
        if file_name.endswith('.jpg'):
            file_path = os.path.join(folder, file_name)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width != height:
                        print(f"Removing non-square image: {file_name} ({width}x{height})")
                        os.remove(file_path)
            except Exception as e:
                print(f"Error processing image {file_name}: {e}")

# Resizes images to a specified width and height. This is a destructive process.
def resize_images(folder, new_width, new_height):
    for file_name in os.listdir(folder):
        if file_name.endswith('.jpg'):
            file_path = os.path.join(folder, file_name)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width != new_height and height != new_height:
                        # Resize image while maintaining aspect ratio
                        img.thumbnail((new_width, new_height))
                        # Save the resized image
                        img.save(file_path)
                        print(f"Resized image: {file_name}")
            except Exception as e:
                print(f"Error processing image {file_name}: {e}")

# Sorts images by a specified X value (brightness, saturation, hue)
def sort_images_by_X (images, X):
    if X == 'brightness':
        images_with_X = [(image, calculate_average_brightness_inverted(image)) for image in images]
    elif X == 'saturation':
        images_with_X = [(image, calculate_average_saturation(image)) for image in images]
    elif X == 'hue':
        images_with_X = [(image, calculate_average_hue(image)) for image in images]
    else:
        print(f"Did not recognize {X} as a sorting criteria. Options are 'brightness', 'saturation', and 'hue'.")
        sys.exit()

    if reverse == False:
        images_with_X.sort(key=lambda x: x[1], reverse=False)
    elif reverse == True:
        images_with_X.sort(key=lambda x: x[1], reverse=True)

    sorted_images = [image for image, value in images_with_X]
    return sorted_images

# Calculates the number of album covers per side based on the total number of images.
def calculate_num_album_covers_per_side():
    # Gets the number of files in the folder
    num_images = len(os.listdir('album_covers'))
    # Suppose we have 4950 images. The first square number greater than 4950 is 70^2 = 4900.
    # Hence, we take the square root of the number of albums and then floor this number
    num_album_covers_per_side = int(num_images ** 0.5)
    return num_album_covers_per_side

# Calculates 1 - the average brightness value for an image
# The purpose of this inversion is to make the default sorting order descending
def calculate_average_brightness_inverted (image_path):
    with Image.open(image_path) as img:
        # Convert image to grayscale
        gray_img = img.convert('L')
        # Calculate mean pixel value
        mean_pixel_value = ImageStat.Stat(gray_img).mean[0]
        # Normalize brightness to range [0, 1]
        brightness = mean_pixel_value / 255
        return 1 - brightness

def calculate_average_saturation(image_path):
    with Image.open(image_path) as img:
        # Convert the image to the RGB color space if it's not already in RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')

        saturation_sum = 0
        pixel_count = 0

        # Iterate through the pixels of the image
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                # Convert the RGB color to HSV
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                # Add the saturation value to the saturation sum
                saturation_sum += s
                pixel_count += 1

        # Calculate the average saturation
        average_saturation = saturation_sum / pixel_count
        return average_saturation

def calculate_average_hue(image_path):
    with Image.open(image_path) as img:
        # Convert the image to the RGB color space if it's not already in RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')

        hue_sum = 0
        pixel_count = 0

        # Iterate through the pixels of the image
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                # Convert the RGB color to HSV
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                # Add the hue value to the hue sum
                hue_sum += h
                pixel_count += 1

        # Calculate the average hue
        average_hue = hue_sum / pixel_count
        return average_hue

# Used to rank all midpoints where albums get placed by their distance from the center of the collage
def calculate_distance_to_center(width, num_album_covers_width, num_album_covers_height):
    piece_midpoint = [(width * num_album_covers_width) / 2, (width * num_album_covers_height) / 2]
    # function that calculates the distance between two points
    def getDistance(x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    midpoints = {}
    for j in range(num_album_covers_height):
        for i in range(num_album_covers_width):
            midpoints[(i,j)] = ((width * i) + (width / 2), (width * j) + (width / 2))

    midpoints_distances = {}
    for midpoint in midpoints:
        midpoints_distances[midpoint] = getDistance(midpoints[midpoint][0], midpoints[midpoint][1], piece_midpoint[0], piece_midpoint[1])

    # sort midpoints by distance to center
    midpoints_distances = sorted(midpoints_distances.items(), key=lambda x: x[1])
    return midpoints_distances

# Used to rank all midpoints where albums get placed by their distance from the distance to as specified side
def calculate_distance_to_side(dimension, num_album_covers_width, num_album_covers_height, side):
    midpoints = {}
    for j in range(num_album_covers_height):
        for i in range(num_album_covers_width):
            midpoints[(i,j)] = ((dimension * i) + (dimension / 2), (dimension * j) + (dimension / 2))

    midpoints_distances = {}
    for midpoint in midpoints:
        if side == 'left':
            midpoints_distances[midpoint] = midpoints[midpoint][0]
        elif side == 'right':
            midpoints_distances[midpoint] = (dimension * num_album_covers_width) - midpoints[midpoint][0]
        elif side == 'top':
            midpoints_distances[midpoint] = midpoints[midpoint][1]
        elif side == 'bottom':
            midpoints_distances[midpoint] = (dimension * num_album_covers_height) - midpoints[midpoint][1]
        else:
            print("Invalid side")

    midpoints_distances = sorted(midpoints_distances.items(), key=lambda x: x[1])
    return midpoints_distances

# Creates the final collage image using the arranged images.
def create_collage(images, num_album_covers_width, num_album_covers_height, dimension):
    # Create a new blank image with enough space for the collage
    collage = Image.new('RGB', (dimension * num_album_covers_width, dimension * num_album_covers_height))
    
    # Get the sorted list of midpoints distances
    midpoints_distances = calculate_distance_to_center(dimension, num_album_covers_width, num_album_covers_height,)

    # CHANGE ME: Comment the line above and uncomment the two lines below to sort by distance to a side
    # side = "top"
    # midpoints_distances = calculate_distance_to_side(dimension, num_album_covers_width, num_album_covers_height, side)
    
    # Paste each image into the collage at the corresponding midpoint
    for idx, (midpoint, distance) in enumerate(midpoints_distances):
        if idx < len(images):
            image_path = images[idx]
            with Image.open(image_path) as img:
                x, y = midpoint
                collage.paste(img, (x * dimension, y * dimension))

    # Save the final collage
    collage.save('collage.jpg')
    print("Collage created and saved as collage.jpg")


# Sorts along two axises
def create_collage_double_sorted(images, num_album_covers_width, num_album_covers_height, dimension):
    # CHANGE ME: These are the parameters for the double sort
    first_sort_criteria = "saturation"
    second_sort_criteria = "hue"
    first_sort_direction = "left"
    second_sort_direction = "top"

    images = sort_images_by_X(images, first_sort_criteria)
    
    # Create a new blank image with enough space for the collage
    collage = Image.new('RGB', (dimension * num_album_covers_width, dimension * num_album_covers_height))
    
    # Get the sorted list of midpoints distances
    # midpoints_distances = calculate_distance_to_center(width, num_album_covers_per_side)
    midpoints_distances = calculate_distance_to_side(dimension, num_album_covers_width, num_album_covers_height, first_sort_direction)

    for i in range(0, len(images), num_album_covers_width):
        images_slice = images[i:i+num_album_covers_width]

        sorted_images = sort_images_by_X(images_slice, second_sort_criteria)

        for j in range(0, len(sorted_images), 1):
            image_path = sorted_images[j]

            midpoint, distance = midpoints_distances[i + j]
            x, y = midpoint
            with Image.open(image_path) as img:

                if second_sort_direction == "left":
                    collage.paste(img, (j * dimension, y * dimension))
                elif second_sort_direction == "right":
                    collage.paste(img, ((num_album_covers_width - j) * dimension, y * dimension))
                elif second_sort_direction == "top":
                    collage.paste(img, (x * dimension, j * dimension))
                elif second_sort_direction == "bottom":
                    collage.paste(img, (x * dimension, (num_album_covers_height - j) * dimension))

    # Save the final collage
    collage.save('collage.jpg')
    print("Collage created and saved as collage.jpg")

global reverse
def main(argv):
    global reverse
    reverse = False
    sort_criteria = "brightness"
    image_dimension = 64 # default image dimension

     # Check if arguments are passed
    if len(argv) > 0:
        if argv[-1] == "--reverse":
            reverse = True

        if len(argv) > 1:
            if argv[0] == "hue" or argv[1] == "hue":
                sort_criteria = "hue"
            if argv[0] == "saturation" or argv[1] == "saturation":
                sort_criteria = "saturation"
        else:
            if argv[0] == "hue":
                sort_criteria = "hue"
            elif argv[0] == "saturation":
                sort_criteria = "saturation"
        
        if argv[0] != "--reverse" and argv[0] != "hue" and argv[0] != "saturation" and argv[0] != "brightness":
            image_dimension = int(argv[0])

    if image_dimension < 0 or image_dimension > 640:
        print("Something went wrong with the image dimension")
        return
    
    resize_images('album_covers', image_dimension, image_dimension)

    num_album_covers_per_side = calculate_num_album_covers_per_side()
    # Default output is a square. Change values below and comment the line above to make a rectangle
    num_album_covers_width = num_album_covers_per_side
    num_album_covers_height = num_album_covers_per_side

    folder = 'album_covers'
    images = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.jpg')]

    exact_albums_needed = num_album_covers_width * num_album_covers_height
    if (exact_albums_needed) > len(images):
        images = images[:exact_albums_needed]

    sorted_images = sort_images_by_X(images, sort_criteria)
    create_collage(sorted_images, num_album_covers_width, num_album_covers_height, image_dimension)

    # CHANGE ME: Comment the two line above and uncomment the line below to sort along two axises (double sort)
    # create_collage_double_sorted(images, num_album_covers_width, num_album_covers_height, image_dimension)

if __name__ == "__main__":
    main(sys.argv[1:])


