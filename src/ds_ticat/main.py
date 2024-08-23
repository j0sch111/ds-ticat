import json

from germansentiment import SentimentModel
from Greetingfilter import Greetingfilter
from TextPreProcessor import TextPreProcessor
from TextTokenizer import TextTokenizer

event = {
    "Item": {
        "ticket_id": {"N": "2720903312"},
        "content": {"S": "Ich liebe SevDESK, mein Freund! Mit freundlichen Gruß"},
    }
}
greet_file = "/Users/sebastianrose/Documents/Repos/ds-tisent/configs/greetings_test.yaml"

# load content from Event
content = event["Item"]["content"]["S"]

# Text preprocessing
processed_conntent = TextPreProcessor.process_text(content)
print("step1:", processed_conntent)
# Greeting cutting
content_wo_greetings = Greetingfilter.cut_after_greetings(processed_conntent, greet_file, key_name="greetings")
print("step2:", content_wo_greetings)
# Tokenizer
final_content = TextTokenizer.tokenize_text(content_wo_greetings)
print("step final:", final_content, type(final_content))

model = SentimentModel()
sentiment_label = model.predict_sentiment([final_content])

event["Item"]["sentiment"] = {"S": sentiment_label}

event_json = json.dumps(event)
print(event_json)
