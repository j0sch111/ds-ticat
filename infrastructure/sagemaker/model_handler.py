from inference_handler import ContainerModelInferenceHandler
from sagemaker_inference import transformer
from sagemaker_inference.default_handler_service import DefaultHandlerService


# For the one model use case, this points to the InferenceHandler class which
# defines the default functions for loading, predicting, and serializing the model.
class HandlerService(DefaultHandlerService):
    def __init__(self):
        tr = transformer.Transformer(default_inference_handler=ContainerModelInferenceHandler())
        super(HandlerService, self).__init__(transformer=tr)
