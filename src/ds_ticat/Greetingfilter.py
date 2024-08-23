from TextPreProcessor import TextPreProcessor


class GreetingProcessor:
    def load_and_process_greetings_sequences(self, greetings_file):
        """
        Load and clean greeting sequences from a file.
        """
        try:
            # Load list of strings from file
            with open(greetings_file, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Clean lines by stripping whitespace and filtering out empty lines
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            print(f"{greetings_file} loaded successfully.")

            # Further process the cleaned lines using process_text
            if cleaned_lines:
                processed_greetings_sequences = [line.replace('"', "").replace(",", "") for line in cleaned_lines]
                processed_greetings_sequences = TextPreProcessor.process_text(processed_greetings_sequences)

            return processed_greetings_sequences

        except FileNotFoundError:
            print(f"Error: '{greetings_file}' file not found.")
        except Exception as e:
            print(f"An error occurred while processing greetings_sequences: {e}")

    def cut_after_greetings_sequences(self, text, greetings_sequences):
        """
        Cuts the text after any greeting found in the text.
        """
        try:
            for greeting in greetings_sequences:
                if greeting in text:
                    return text.split(greeting)[0].strip()
            return text
        except Exception as e:
            print(f"An error occurred while cutting after greetings sequences: {e}")
            return text
