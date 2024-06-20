from io import BytesIO
from base64 import b64decode
from openai import OpenAI
from PIL import Image


def get_selected_text() -> str:
    """
    Prompts the user to input selected text, validates its length, and returns the text if valid.

    Returns:
        str: The selected text provided by the user.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        The function prompts the user to paste their selected text, which
        should be less than 600 characters.
        If the input is empty or exceeds 600 characters, it prompts again
        recursively until valid input is provided.
    """
    try:
        sel_text = input(
            "Paste your selected text here (should be less than a 600 characters):\n"
        )
        if 0 >= len(sel_text) > 600:
            print("Selected text cannot be empty nor can it exceed 1000 charcters!")
            sel_text = get_selected_text()
            return sel_text
        return sel_text
    except Exception as err:
        print("Error encountered: ", err)


def get_user_prompts() -> str:
    """
    Prompts the user to choose or input a prompt for visualizing selected text.

    Returns:
        str: The selected or custom prompt provided by the user.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        The function presents a menu of predefined prompts and allows the user to select
        one of them or enter a custom prompt. It validates the input and ensures the prompt
        does not exceed 280 characters (excluding punctuation). If the input is invalid,
        it prompts again recursively until valid input is provided.
    """
    try:
        choice = input(
            """Given below are some prompts to visualize the selected text,
                you can select any of them or write your own prompt- \n
                1. Create a highly detailed and vibrant image that captures the essence 
                of the following description, considering all elements and nuances mentioned: Press 1\n
                2. Generate a realistic and intricate visual representation based on this 
                prompt, ensuring to include all key details and characteristics described: Press 2\n
                3. Visualize the scene described in the following text with great attention
                to detail, focusing on accurately depicting the environment, characters, 
                and any specific features mentioned: Press 3\n
                4. Illustrate the following concept as described, with a high level of
                detail and precision, ensuring that all aspects of the text 
                are faithfully represented: Press 4\n
                5. Write your own custom prompt: Press 5\n
                Your Choice: 
                """
        )
        match choice:
            case "1":
                sel_prompt = """Create a highly detailed and vibrant image that captures the essence
                                nuances mentioned.\n"""
                return sel_prompt
            case "2":
                sel_prompt = """Generate a realistic and intricate visual representation based
                                on this prompt, ensuring to include all key details and 
                                characteristics described.\n"""
                return sel_prompt
            case "3":
                sel_prompt = """Generate a realistic and intricate visual
                                representation based on this prompt, ensuring 
                                to include all key details and characteristics 
                                described.\n"""
                return sel_prompt
            case "4":
                sel_prompt = """Illustrate the following concept as described,
                                with a high level of detail and precision,
                                ensuring that all aspects of the text are
                                faithfully represented.\n"""
                return sel_prompt
            case "5":
                sel_prompt = input("Your prompt within 280 characters: \n")
                sel_prompt = sel_prompt + "." + "\n"
                if len(sel_prompt) > 280:
                    print(
                        "Your prompt exceed the 300 character limit, it has {} characters.\n Try again".format(
                            len(sel_prompt)
                        )
                    )
                    sel_prompt = get_user_prompts()
                return sel_prompt
            case _:
                print("Invalid input for prompt selection, please try again.")
                sel_prompt = get_user_prompts()
                return sel_prompt

    except Exception as err:
        print("Error encountered: ", err)


def get_complete_prompt(sel_text: str, user_prompt: str):
    """
    Generates a complete prompt by combining user-provided prompt and selected text.

    Args:
        sel_text (str): The selected text to be described in the prompt.
        user_prompt (str): The user-provided prompt for visualizing the selected text.

    Returns:
        str: The complete prompt combining user_prompt and sel_text.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function takes in a selected text and a user-provided prompt, and combines them
        to form a complete prompt string. It is intended to be used for generating prompts
        for visualization or description tasks, ensuring that the selected text is accurately
        described or visualized as per the user's prompt.

    Note:
        The pre_cursor is used to ensure that the text-to-image model doesn't manipulate
        prompt sent via api call, for faithful visulization for selected text, however, the
        inclusion of pre_cursor in the final prompt results in erronous images
        that do not match the final prompt at all, as such pre_cursor has been
        commented out.
    """
    try:
        # pre_cursor = "I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS. "
        # complete_prompt = pre_cursor + user_prompt + " Description: " + sel_text
        complete_prompt = user_prompt + " Description: " + sel_text
        return complete_prompt
    except Exception as err:
        print("Error encountered: ", err)
        return False


def get_image(client, user_prompt, image_size="512x512"):
    """
    Generates an image based on the user-provided prompt using an AI image generation API.

    Args:
        client: The client object used to communicate with the image generation service.
        user_prompt (str): The prompt describing the image to be generated.
        image_size (str, optional): The size of the image to be generated, formatted as "heightxwidth".
                                    Defaults to "512x512".

    Returns:
        str: Base64 encoded image data in JSON format.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function interacts with an AI image generation service (specified by `client`)
        to generate an image based on the given user_prompt. The image_size parameter
        determines the dimensions of the image. It returns the base64 encoded image data
        in JSON format. If an error occurs during the image generation process, it prints
        an error message with details.
    """
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=user_prompt,
            size=image_size,
            quality="standard",
            response_format="b64_json",
            n=1,
            timeout=30
        )
        image_b64_json = response.data[0].b64_json
        return image_b64_json
    except Exception as err:
        print("Error encountered: ", err)


def display_image_json(image_b64_json):
    """
    Decodes and displays an image from base64 encoded JSON data.

    Args:
        image_b64_json (str): Base64 encoded image data in JSON format.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function takes base64 encoded image data in JSON format (`image_b64_json`),
        decodes it, and displays the image. It uses libraries like `base64`, `PIL.Image`,
        and `BytesIO` to decode and display the image. If an error occurs during the
        decoding or displaying process, it prints an error message with details.
    """
    try:
        image_data = b64decode(image_b64_json)
        img = Image.open(BytesIO(image_data))
        img.show()
    except Exception as err:
        print("Error encountered: ", err)


def main(client):
    """
    Executes a series of functions to generate and display an image based on user inputs.

    Args:
        client: The client object used to interact with external services for image generation.

    Raises:
        This function handles exceptions internally and prints the error message.

    Usage:
        This function serves as the main entry point for generating and displaying an image
        based on user inputs. It sequentially calls the following functions:
        - `get_selected_text()`: Prompts the user to input selected text.
        - `get_user_prompts()`: Prompts the user to select or input a prompt for visualizing the text.
        - `get_complete_prompt(sel_text, sel_prompt)`: Combines selected text and user prompt into a complete prompt.
        - `get_image(client, prompt, image_size="512x512")`: Generates an image based on the complete prompt.
        - `display_image_json(image_b64_json)`: Decodes and displays the generated image from base64 encoded JSON data.

        If any error occurs during the execution of these functions, it catches the exception
        and prints an error message with details.
    """
    try:
        sel_txt = get_selected_text()
        sel_prompt = get_user_prompts()
        prompt = get_complete_prompt(sel_txt, sel_prompt)
        img_file = get_image(client, prompt, image_size="512x512")
        display_image_json(img_file)
    except Exception as err:
        print("Error encountered: ", err)


if __name__ == "__main__":
    client = OpenAI(api_key="your api key goes here")
    main(client)
