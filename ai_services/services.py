import google.generativeai as genai
from django.conf import settings
from PIL import Image
import fitz  # PyMuPDF
import io


def get_gemini_vision_response(image_path: str, prompt: str) -> str:
    """
    Takes an image path and a text prompt, and returns the response
    from the Gemini Pro Vision model.

    Args:
        image_path: The absolute path to the image file.
        prompt: The text prompt to send with the image.

    Returns:
        The text response from the API.

    Raises:
        Exception: If the API call fails for any reason.
    """
    try:
        # 1. Configure the API client
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # 2. Open the image file
        img = Image.open(image_path)

        # 3. Create the vision model instance
        model = genai.GenerativeModel('gemini-pro-vision')

        # 4. Generate content
        response = model.generate_content([prompt, img])

        # 5. Add a check to ensure the response has text
        if not response.parts:
            raise Exception("The API returned a response with no parts (it may have been blocked).")

        return response.text
    except Exception as e:
        # Re-raise the exception to be handled by the calling view
        raise Exception(f"Gemini API Error: {e}")


def get_gemini_text_response(text_input: str, prompt: str) -> str:
    """
    Takes a block of text and a prompt, and returns a response
    from the Gemini Pro model. Ideal for summarization, analysis, etc.

    Args:
        text_input: The block of text to analyze or summarize.
        prompt: The specific instruction for the model (e.g., "Summarize this text").

    Returns:
        The text response from the API.

    Raises:
        Exception: If the API call fails for any reason.
    """
    try:
        # 1. Configure the API client
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # 2. Create the text model instance
        model = genai.GenerativeModel('gemini-pro')

        # 3. Combine the prompt and the text for the API call
        full_prompt = f"{prompt}\n\n---\n\n{text_input}"

        # 4. Generate content
        response = model.generate_content(full_prompt)

        # 5. Add a check for an empty response
        if not response.parts:
            raise Exception("The API returned a response with no parts (it may have been blocked).")

        return response.text
    except Exception as e:
        # Re-raise the exception to be handled by the calling view
        raise Exception(f"Gemini API Error: {e}")


def get_gemini_pdf_text_response(pdf_path: str, prompt: str) -> str:
    """
    (Basic Method) Extracts text from a PDF file and sends it to the Gemini Pro model
    for analysis. Best for text-heavy, simple-layout documents.

    Args:
        pdf_path: The absolute path to the PDF file.
        prompt: The specific instruction for the model (e.g., "Summarize this document").

    Returns:
        The text response from the API.

    Raises:
        Exception: If the PDF can't be read or the API call fails.
    """
    try:
        # 1. Extract text from the PDF using PyMuPDF (fitz)
        full_text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                full_text += page.get_text()

        if not full_text.strip():
            raise Exception("Could not extract any text from the PDF.")

        # 2. Call the existing text response function with the extracted text
        return get_gemini_text_response(text_input=full_text, prompt=prompt)

    except Exception as e:
        # Re-raise the exception to be handled by the calling view
        raise Exception(f"PDF Processing or API Error: {e}")


def get_gemini_pdf_multimodal_response(pdf_path: str, prompt: str) -> str:
    """
    (Advanced Method) Mimics the Gemini chat interface by converting each PDF page
    into an image and sending the sequence of images to the Gemini Pro Vision model.
    Excellent for PDFs with complex layouts, tables, and images.

    Args:
        pdf_path: The absolute path to the PDF file.
        prompt: The specific instruction for the model (e.g., "Summarize this document based on its pages").

    Returns:
        The text response from the API.

    Raises:
        Exception: If the PDF can't be read or the API call fails.
    """
    try:
        # 1. Configure the API client
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro-vision')

        # 2. Prepare the request content list, starting with the prompt
        request_parts = [prompt]

        # 3. Open the PDF and convert each page to an image
        with fitz.open(pdf_path) as doc:
            if not doc.page_count:
                raise Exception("PDF has no pages.")

            for page_num, page in enumerate(doc):
                # Render page to a pixmap (a raster image)
                pix = page.get_pixmap()

                # Convert pixmap to bytes
                image_bytes = pix.tobytes("png")

                # Create a PIL Image object from bytes
                img = Image.open(io.BytesIO(image_bytes))

                # Add the PIL image to our request
                request_parts.append(img)

        # 4. Generate content with the list of prompt + images
        response = model.generate_content(request_parts)

        # 5. Check for a valid response
        if not response.parts:
            raise Exception("The API returned a response with no parts (it may have been blocked).")

        return response.text

    except Exception as e:
        raise Exception(f"PDF Multimodal Processing or API Error: {e}")

