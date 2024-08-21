from sagemaker_inference import model_server

HANDLER_SERVICE = "/opt/ml/code/sagemaker/model_handler.py:handle"


def main():
    model_server.start_model_server(handler_service=HANDLER_SERVICE)


if __name__ == "__main__":
    main()
