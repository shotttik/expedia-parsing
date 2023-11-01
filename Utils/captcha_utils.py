import requests
import warnings
import whisper
import tempfile
import os


CAPTCHA_URL = 'security/check'


class CaptchaUtils:

    @staticmethod
    def transcribe(url) -> str:
        warnings.filterwarnings("ignore")
        MODEL = whisper.load_model("base")
        # Create a temporary file in binary write mode
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # Write the content from the URL to the temporary file
            temp_file.write(requests.get(url).content)
            temp_file_name = temp_file.name

        # Now, you can use the 'temp_file_name' as the input to your 'model.transcribe' function
        result = MODEL.transcribe(temp_file_name)

        # Don't forget to clean up the temporary file once you're done with it
        os.remove(temp_file_name)

        # Return the result
        return result["text"].strip()
