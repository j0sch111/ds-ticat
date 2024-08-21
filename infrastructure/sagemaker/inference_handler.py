import json
import logging
import os
from sagemaker_inference import default_inference_handler
from ds_ticat.ModelManager import ModelManager

logging.basicConfig(level=logging.DEBUG)
MODEL_ID = "sentiment_analysis_model"

class ContainerModelInferenceHandler(default_inference_handler.DefaultInferenceHandler):
    def __init__(self):
        self.model_manager = None

    def default_model_fn(self, model_dir):
        logging.info(f"Loading model from directory: {model_dir}")
        self.model_manager = ModelManager(
            project_root="/opt/ml",
            model_dir=model_dir,
            data_dir="/opt/ml/input/data/"
        )
        self.model_manager.load_model()
        logging.info("Model loaded successfully")
        return self.model_manager
    def default_input_fn(self, data, content_type):
        data_string = str(data)
        logging.debug(f"Deserializing the input data. Content type: {content_type}")
        if content_type == "application/json":
            logging.debug(f"Deserializing the input data {data_string}.")
            decoded_data = json.loads(data_string)
            logging.debug(f"Deserialized input data: {decoded_data}.")

            if isinstance(decoded_data, dict) and 'text' in decoded_data:
                return decoded_data['text']
            elif isinstance(decoded_data, str):
                return decoded_data
            else:
                raise ValueError("Input data should be a string or a dictionary with 'text' key.")
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def default_predict_fn(self, input_data, model_manager):
        logging.debug(f"Predicting for input data: {input_data}")
        label, confidence = model_manager.predict(input_data)
        logging.debug(f"Prediction: {label}, Confidence: {confidence}")
        return [label, confidence, MODEL_ID]

    def default_output_fn(self, prediction_output, accept):
        logging.debug(f"Serializing the generated output {prediction_output}")
        if accept == "application/json":
            serialized_prediction = {
                "label": prediction_output[0],
                "confidence": float(prediction_output[1]),
                "model_id": prediction_output[2],
            }
            return json.dumps(serialized_prediction)
        else:
            raise ValueError(f"Unsupported accept type: {accept}")

    def handle(self, data, context):
        """Handle the request."""
        model_name = context.model_name
        logging.info(f"Handling request with model: {model_name}")

        # The rest of the method remains the same
        model = self.default_model_fn(context.model_dir)
        input_data = self.default_input_fn(data, context.request_content_type)
        prediction = self.default_predict_fn(input_data, model)
        result = self.default_output_fn(prediction, context.accept)

        return result
