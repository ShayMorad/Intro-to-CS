


##############################################################################
#                                   Imports                                  #
##############################################################################
import copy
import sys
from ex5_helper import *
from typing import Optional
from math import floor


##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """Separates a colored image to different channels."""
    index = len(image[0][0])
    image_lst = []
    for i in range(index):
        temp_row = []
        for row in image:
            temp_col = []
            for col in row:
                temp_col.append(col[i])
            temp_row.append(temp_col)
        image_lst.append(temp_row)
    return image_lst


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    "Combines separated image channels."
    return separate_channels(separate_channels(channels))


def combine_channels1(channels: List[SingleChannelImage]) -> ColoredImage:
    combined = list()

    # how many columns indexes
    columns_indexes = len(channels[0])
    # how many rows indexes
    rows_indexes = len(channels)
    # how many nums indexes
    nums_indexes = len(channels[0][0])

    for col_i in range(columns_indexes):
        temp_row = list()
        for i in range(nums_indexes):
            temp_col = list()
            for row_i in range(rows_indexes):
                temp_col.append(channels[row_i][col_i][i])
            temp_row.append(temp_col)
        combined.append(temp_row)
    return combined


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """Transforms an RGB image to a grayscale image."""

    # how many columns indexes
    columns_indexes = len(colored_image[0])
    # how many rows indexes
    rows_indexes = len(colored_image)
    gray_scale = list()
    for row_i in range(rows_indexes):
        temp_row = list()
        for col_i in range(columns_indexes):
            red = (colored_image[row_i][col_i][0]) * 0.299
            green = (colored_image[row_i][col_i][1]) * 0.587
            blue = (colored_image[row_i][col_i][2]) * 0.114
            temp_row.append(round(red + green + blue))
        gray_scale.append(temp_row)
    return gray_scale


def blur_kernel(size: int) -> Kernel:
    """Makes a blur kernel by a given whole size."""
    kernel = list()
    for col in range(size):
        temp_col = list()
        for i in range(size):
            temp_col.append(1 / (size ** 2))
        kernel.append(temp_col)
    return kernel


def calculate_pixel_kernel(image, pixel_row_index, pixel_column_index, kernel):
    """Calculates padded pixel by a given kernel"""
    kernel_size = len(kernel) - 1
    kernel_mid = kernel_size // 2
    sum_of_center_pixel = 0
    for row_i in range(kernel_size + 1):
        for col_i in range(kernel_size + 1):
            curr_row = pixel_row_index - kernel_mid + row_i
            curr_col = pixel_column_index - kernel_mid + col_i
            if curr_row < 0 or curr_col < 0 or curr_row > len(image) - 1 or curr_col > (len(image[0]) - 1):
                curr_pixel = image[pixel_row_index][pixel_column_index]
                pixel_pad = curr_pixel * kernel[row_i][col_i]
                sum_of_center_pixel += pixel_pad
            else:
                curr_pixel = image[curr_row][curr_col]
                pixel_pad = curr_pixel * kernel[row_i][col_i]
                sum_of_center_pixel += pixel_pad
    if sum_of_center_pixel < 0:
        sum_of_center_pixel = 0
    elif sum_of_center_pixel > 255:
        sum_of_center_pixel = 255
    return round(sum_of_center_pixel)


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """Applies a kernel padding to an image."""
    padded_image = copy.deepcopy(image)
    for row_i in range(len(image)):
        for col_i in range(len(image[0])):
            padded_pixel = calculate_pixel_kernel(image, row_i, col_i, kernel)
            padded_image[row_i][col_i] = padded_pixel
    return padded_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """Calculates an interpolated pixel by a given coordinate in an image."""
    backward_column_index = int(x)
    forward_column_index = backward_column_index + 1
    backward_row_index = int(y)
    forward_row_index = backward_row_index + 1
    if y == int(y):
        backward_row_index = int(y)
        forward_row_index = int(y)
    if x == int(x):
        backward_column_index = int(x)
        forward_column_index = int(x)
    if forward_column_index > len(image[0]) - 1:
        forward_column_index = len(image[0]) - 1
    if forward_row_index > len(image) - 1:
        forward_row_index = len(image) - 1

    # a = backrow, backcol, b = forwardrow,backcol, c = backrow, forwardcol, d = forwardrow, forwardcol
    pixel_a = image[backward_row_index][backward_column_index]
    pixel_b = image[forward_row_index][backward_column_index]
    pixel_c = image[backward_row_index][forward_column_index]
    pixel_d = image[forward_row_index][forward_column_index]
    if y > 1:
        delta_y = y - backward_row_index
    else:
        delta_y = y
    if x > 1:
        delta_x = x - backward_column_index
    else:
        delta_x = x
    interpolated_pixel = pixel_a * (1 - delta_x) * (1 - delta_y) + pixel_b * (delta_y) * (1 - delta_x) + pixel_c * (
        delta_x) * (1 - delta_y) + pixel_d * delta_x * delta_y
    if interpolated_pixel > 255:
        interpolated_pixel = 255
    elif interpolated_pixel < 0:
        interpolated_pixel = 0
    return round(interpolated_pixel)


def create_empty_destination_for_resize(height, width):
    """Creates an empty image destination for the resize function."""
    empty_image = []
    for row in range(height):
        temp_row = []
        for col in range(width):
            temp_row.append(0)
        empty_image.append(temp_row)
    return empty_image


def change_corner_pixels_for_destination_image(original_image, destination_image):
    """Replaces the corners in the destination image for the resize function with the pixels from the original image."""
    destination_image[0][0] = original_image[0][0]
    destination_image[-1][0] = original_image[-1][0]
    destination_image[0][-1] = original_image[0][-1]
    destination_image[-1][-1] = original_image[-1][-1]
    return destination_image


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """Changes image size based on input height and width."""
    destination_image = change_corner_pixels_for_destination_image(image,
                                                                   create_empty_destination_for_resize(new_height,
                                                                                                       new_width))
    for row_i in range(len(destination_image)):
        for col_i in range(len(destination_image[0])):
            # skip corner pixels
            if row_i == 0 and col_i == 0:
                continue
            elif row_i == 0 and col_i == (len(destination_image[0]) - 1):
                continue
            elif row_i == (len(destination_image) - 1) and (col_i == 0):
                continue
            elif row_i == (len(destination_image) - 1) and col_i == (len(destination_image[0]) - 1):
                continue
            else:
                y = (row_i / (len(destination_image) - 1)) * (len(image) - 1)
                x = (col_i / (len(destination_image[0]) - 1)) * (len(image[0]) - 1)
                destination_image[row_i][col_i] = bilinear_interpolation(image, y, x)
    return destination_image


def rotate_90(image: Image, direction: str) -> Image:
    """Rotates an image (2D or 3D) 90 degrees in the given direction, 'L' for left and 'R' for right."""

    rotated_image = []
    columns = len(image[0])
    if direction == "R":
        for col in range(columns):
            temp_row = []
            for row in image[::-1]:
                temp_row.append(row[col])
            rotated_image.append(temp_row)
    elif direction == "L":
        for col in range(columns - 1, -1, -1):
            temp_row = []
            for row in image:
                temp_row.append(row[col])
            rotated_image.append(temp_row)
    return rotated_image


def calculate_threshold(image, pixel_row_index, pixel_column_index, kernel):
    """Calculates padded pixel by a given kernel"""
    kernel_size = len(kernel) - 1
    kernel_mid = kernel_size // 2
    threshold = 0
    for row_i in range(kernel_size + 1):
        for col_i in range(kernel_size + 1):
            curr_row = pixel_row_index - kernel_mid + row_i
            curr_col = pixel_column_index - kernel_mid + col_i
            if curr_row < 0 or curr_col < 0 or curr_row > len(image) - 1 or curr_col > (len(image[0]) - 1):
                curr_pixel = image[pixel_row_index][pixel_column_index]
                threshold += curr_pixel
            else:
                curr_pixel = image[curr_row][curr_col]
                threshold += curr_pixel
    threshold = (threshold) / ((kernel_size + 1) * (kernel_size + 1))
    return threshold


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """Returns the input image with only its outlines, in black. Other pixels are white."""
    kernel_for_blur = blur_kernel(blur_size)
    blurred_image = apply_kernel(image, kernel_for_blur)
    edged_image = copy.deepcopy(blurred_image)
    kernel_for_threshold = blur_kernel(block_size)
    for row_i in range(len(blurred_image)):
        for col_i in range(len(blurred_image[0])):
            pixel = blurred_image[row_i][col_i]
            threshold_before_c = calculate_threshold(blurred_image, row_i, col_i, kernel_for_threshold)
            threshold_minus_c = threshold_before_c - c
            if pixel < threshold_minus_c:
                edged_image[row_i][col_i] = 0
            else:
                edged_image[row_i][col_i] = 255
    return edged_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """Quantize an image based on input channels."""
    quantized_image = []
    for row in image:
        temp_row = []
        for pixel in row:
            quantized_pixel = round((floor(pixel * (N / 256))) * (255 / (N - 1)))
            temp_row.append(quantized_pixel)
        quantized_image.append(temp_row)
    return quantized_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """Quantize a colored image based on input channels."""
    separated_channels = separate_channels(image)
    quantized_separated_channels = []
    for channel in separated_channels:
        quantized_channel = quantize(channel, N)
        quantized_separated_channels.append(quantized_channel)
    combined_quantized_channels = combine_channels(quantized_separated_channels)
    return combined_quantized_channels


def get_load_image_mode():
    """Gets load mode for input image by the user."""
    load_mode = input("What mode do you want to load the image in? \n'L' for grayscale, 'RGB' for rgb: ")
    print()
    while load_mode not in ['L', 'RGB']:
        print("Wrong input!\n")
        load_mode = input("What mode do you want to load the image in? \n'L' for grayscale, 'RGB' for rgb: ")
    print()
    return load_mode


def get_edit_action_on_image():
    """Asks the user what action to perform."""
    edit_action = input("These are the following possible actions to perform on the loaded image:\n"
                        "1. Transform a colored image to a grayscale image.\n"
                        "2. Blur image.\n"
                        "3. Resize image.\n"
                        "4. Rotate image (90 degrees, left or right).\n"
                        "5. Transform image to its edges.\n"
                        "6. Quantize image.\n"
                        "7. Show image.\n"
                        "8. Exit program.\n"
                        "Enter 1-8 to choose the wanted action: ")
    print()
    if edit_action not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        while edit_action not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("Wrong input.\n")
            edit_action = input("These are the following possible actions to perform on your current loaded image:\n"
                                "1. Transform a colored image to a grayscale image.\n"
                                "2. Blur image.\n"
                                "3. Resize image.\n"
                                "4. Rotate image (90 degrees, left or right).\n"
                                "5. Transform image to its edges.\n"
                                "6. Quantize image.\n"
                                "7. Show image.\n"
                                "8. Exit program.\n"
                                "Enter 1-8 to choose the wanted action: ")
    print()
    return edit_action


def action_1(loaded_image):
    """Convert input colored image to a grayscale image."""
    try:
        x = loaded_image[0][0][0]
        grayscale_image = RGB2grayscale(loaded_image)
        print("Image was converted to grayscale!\n")
        return grayscale_image
    except:
        print("Image is already in grayscale.\n"
              "No changes were made.\n")
        return loaded_image


def action_2(loaded_image):
    """Blurs loaded image."""
    user_kernel_size = input("Please enter kernel size for blurring.\n"
                             "Kernel size must be a positive, uneven integer: ")
    print()
    try:
        int(user_kernel_size)
    except:
        print("Wrong kernel size.. Quitting action...\n")
        return loaded_image
    if int(user_kernel_size) >= 1 and (int(user_kernel_size) % 2 == 1) and (int(user_kernel_size) % 1 == 0):
        user_kernel_size = int(user_kernel_size)
        kernel = blur_kernel(user_kernel_size)
        try:
            x = loaded_image[0][0][0]
            separated_channels = separate_channels(loaded_image)
            separated_channels_blurred = []
            for channel in separated_channels:
                blurred_channel = apply_kernel(channel, kernel)
                separated_channels_blurred.append(blurred_channel)
            combined_blurred_channels = combine_channels(separated_channels_blurred)
            print("..... colored image blurred!\n")
            return combined_blurred_channels
        except:
            blurred_image = apply_kernel(loaded_image, kernel)
            print("..... grayscale image blurred!\n")
            return blurred_image
    else:
        print("Wrong kernel size.. Quitting action...\n")
        return loaded_image


def action_3(loaded_image):
    """Resizes input image."""
    user_input = input("Please enter desired height and width for the new image.\n"
                       "Format must be 'height,width' and values must be whole and bigger than 1: ")
    print()
    if "," not in user_input:
        print("Wrong format size.. Quitting action...!\n")
        return loaded_image
    resize_list = user_input.split(",")
    try:
        height = int(resize_list[0])
        width = int(resize_list[1])
        if height > 1 and width > 1 and (height % 1 == 0) and (width % 1 == 0):
            height = int(height)
            width = int(width)
            try:
                x = loaded_image[0][0][0]
                separated_channels = separate_channels(loaded_image)
                separated_channels_resized = []
                for channel in separated_channels:
                    resized_channel = resize(channel, height, width)
                    separated_channels_resized.append(resized_channel)
                combined_resized_channels = combine_channels(separated_channels_resized)
                print("... image resized!!")
                return combined_resized_channels
            except:
                resized_image = resize(loaded_image, height, width)
                print("... image resized!")
                return resized_image
        else:
            print("Wrong format size.. Quitting action...\n")
            return loaded_image
    except:
        print("Wrong format size.. Quitting action...\n")
        return loaded_image


def action_4(loaded_image):
    """Rotates the input image left or right."""
    user_input = input("Rotate left or right?\n"
                       "Enter 'L' for left, 'R' for right: ")
    print()
    if user_input == "L":
        rotated_image = rotate_90(loaded_image, user_input)
        print("... image rotated!\n")
        return rotated_image
    elif user_input == "R":
        rotated_image = rotate_90(loaded_image, user_input)
        print("... image rotated!\n")
        return rotated_image
    else:
        print("Wrong input.. Quitting action...\n")
        return loaded_image


def action_5(loaded_image):
    """Returns edged image from input image."""
    user_input = input("Please enter a blur size, block size, and a constant.\n"
                       "The correct format is 'blur_size,block_size,constant': ")
    print()
    comma_counter = 0
    for letter in user_input:
        if letter == ",":
            comma_counter += 1
    if comma_counter == 2:
        edges_list = user_input.split(",")
        try:
            blur_size = int(edges_list[0])
            block_size = int(edges_list[1])
            c = float(edges_list[2])
        except:
            print("Wrong format.. Quitting action...\n")
            return loaded_image
        if (blur_size >= 1) and (block_size >= 1) and (blur_size % 2 == 1) and (block_size % 2 == 1) and c >= 0:
            try:
                x = loaded_image[0][0][0]
                grayscaled_image = RGB2grayscale(loaded_image)
                edged_image = get_edges(grayscaled_image, int(blur_size), int(block_size), c)
            except:
                edged_image = get_edges(loaded_image, int(blur_size), int(block_size), c)
            print("... image converted to hyper edges!\n")
            return edged_image
    else:
        print("Wrong format.. Quitting action...\n")
        return loaded_image


def action_6(loaded_image):
    """Quantize input image."""
    user_input = input("How many shades to quantize the image to?\n"
                       "Enter a whole, positive number: ")
    print()
    try:
        n = int(user_input)
    except:
        print("Wrong format.. Quitting action...!\n")
        return loaded_image
    if n > 1 and n % 1 == 0:
        n = int(n)
        if isinstance(loaded_image[0][0], list):
            quantized_image = quantize_colored_image(loaded_image, n)
        else:
            quantized_image = quantize(loaded_image, n)
        print("... image quantized!\n")
        return quantized_image
    else:
        print("Wrong format.. Quitting action...\n")
        return loaded_image


def action_8(loaded_image):
    """Exit program and save image."""
    user_input = input("Please provide a path to save the image to: ")
    save_image(loaded_image, user_input)
    print("... image saved!\n")


if __name__ == '__main__':
    """Run whole program for user."""
    if len(sys.argv) == 2:
        for image_path in sys.argv[1:]:
            # load_mode = get_load_image_mode()
            loaded_image = load_image(image_path)
            exit_ = False
            while not exit_:
                user_wanted_action = get_edit_action_on_image()
                if user_wanted_action == "1":
                    loaded_image = action_1(loaded_image)
                elif user_wanted_action == "2":
                    loaded_image = action_2(loaded_image)
                elif user_wanted_action == "3":
                    loaded_image = action_3(loaded_image)
                elif user_wanted_action == "4":
                    loaded_image = action_4(loaded_image)
                elif user_wanted_action == "5":
                    loaded_image = action_5(loaded_image)
                elif user_wanted_action == "6":
                    loaded_image = action_6(loaded_image)
                elif user_wanted_action == "7":
                    show_image(loaded_image)
                elif user_wanted_action == "8":
                    action_8(loaded_image)
                    print("Thanks for using Shay's image editing tool! >:)")
                    exit_ = True
    elif len(sys.argv) == 1:
        print("No image path was given!\nPlease re-run the program and insert appropriate image path.\n")
    else:
        print(
            "More than one image path was given!\nPlease re-run the program and insert only 1 appropriate image path.\n")
