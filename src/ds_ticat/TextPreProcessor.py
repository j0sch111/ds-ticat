import html
import re


class TextPreProcessor:
    """
    A class used to preprocess text data for various tasks.
    """

    def remove_media_queries(self, text):
        """
        Removes media queries from the text.
        """
        processed_text = re.sub(r"@media[^{]+\{(?:[^{}]+|\{[^{}]*\})*\}", "", text)
        return processed_text

    def remove_cid_images(self, text):
        """
        Removes CID images from the text.
        """
        processed_text = re.sub(r"\[cid:image[^\]]+\]", "", text)
        return processed_text

    def remove_newlines(self, text):
        """
        Replaces newline and carriage return characters in the text with a space.
        """
        processed_text = re.sub(r"[\n\r]+", " ", text)
        return processed_text

    def remove_html_tags(self, text):
        """
        Removes HTML tags from the text.
        """
        processed_text = re.sub(r"<[^>]+>", " ", text)
        return processed_text

    def replace_html_spaces(self, text):
        """
        Replaces HTML non-breaking space entities with a regular space.
        """
        processed_text = re.sub(r"&nbsp;", " ", text)
        return processed_text

    def unescape_html(self, text):
        """
        Converts HTML escape sequences into their corresponding characters.
        """
        processed_text = html.unescape(text)
        return processed_text

    def remove_punctuation(self, text):
        """
        Removes punctuation from the text.
        """
        processed_text = re.sub(r'[,.!?"]+', " ", text)
        processed_text = re.sub(r"[^\w\s]", " ", processed_text, flags=re.UNICODE)
        return processed_text

    def remove_numbers(self, text):
        """
        Removes all digits from the text.
        """
        processed_text = re.sub(r"\d+", " ", text)
        return processed_text

    def normalize_whitespace(self, text):
        """
        Replaces multiple spaces with a single space and trims the text.
        """
        processed_text = re.sub(r"\s+", " ", text).strip()
        return processed_text

    def to_lowercase(self, text):
        """
        Converts all characters in the text to lowercase.
        """
        processed_text = text.lower()
        return processed_text

    def process_text(self, text):
        """
        Processes the text by sequentially applying various preprocessing steps.
        """
        try:
            text = self.remove_media_queries(text)
            text = self.remove_cid_images(text)
            text = self.remove_newlines(text)
            text = self.remove_html_tags(text)
            text = self.replace_html_spaces(text)
            text = self.unescape_html(text)
            text = self.remove_punctuation(text)
            text = self.remove_numbers(text)
            text = self.normalize_whitespace(text)
            text = self.to_lowercase(text)
            return text
        except Exception as e:
            print(f"An error occurred during text processing: {e}")
            return text
