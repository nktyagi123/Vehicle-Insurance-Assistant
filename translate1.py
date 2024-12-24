from transformers import pipeline

def translate_text(text, src_lang="en", tgt_lang="ja"):
    """Translates text from one language to another using a Hugging Face model.

    Args:
        text: The text to be translated.
        src_lang: The source language code.
        tgt_lang: The target language code.

    Returns:
        The translated text.
    """

    model_name = "Helsinki-NLP/opus-mt-en-ja"  # A pre-trained translation model
    translator = pipeline("translation", model=model_name)
    result = translator(text)
    return result[0]["translation_text"]

# Example usage:
text_to_translate = "Hello, how are you?"
translated_text = translate_text(text_to_translate)
print(translated_text)