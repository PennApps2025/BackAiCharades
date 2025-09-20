import requests

# --- Configuration ---
# Make sure your FastAPI server is running at this address.
URL = "http://127.0.0.1:8000/guess"

# The path to the image you want to test with.
# Make sure you have an image file with this name in the same directory.
IMAGE_PATH = "test_image.webp"

# --- Test Data ---
# The correct word the AI should guess.
target_word = "Basketball"

# The list of choices provided to the AI. This must include the target_word.
# This should be a comma-separated string, just like it would be sent from a web form.
choices_str = "Basketball, Soccer, Swimming"

# --- Prepare and Send the Request ---
try:
    # 'files' dictionary for the file upload part of the form.
    # We open the file in binary read mode ('rb').
    files = {"file": open(IMAGE_PATH, "rb")}
    
    # 'data' dictionary for the other form fields.
    data = {
        "word": target_word,
        "choices": choices_str
    }

    print(f"Sending image '{IMAGE_PATH}' with word '{target_word}'...")

    # Send the POST request. 'requests' library handles multipart/form-data encoding automatically.
    response = requests.post(URL, files=files, data=data)

    # Raise an exception if the request returned an error status code (like 4xx or 5xx).
    response.raise_for_status()
    
    # Print the JSON response from the server.
    print("\n--- Server Response ---")
    print(response.json())
    print("-----------------------\n")

except FileNotFoundError:
    print(f"Error: The file '{IMAGE_PATH}' was not found. Please make sure it's in the same directory as the script.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {e}")

finally:
    # It's good practice to ensure the file is closed.
    if 'files' in locals() and files.get('file'):
        files['file'].close()