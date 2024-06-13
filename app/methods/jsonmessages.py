# responses used for processing requests

# success message
def create_success_response(data=None, message=None):
    response ={
        "status": "success",
        "data": data if data is not None else {},
        "message": message
    }
    return response



# error message
def create_error_reponse(message, data=None):
    response = {
        "status": "error",
        "data": data if data is not None else {},
        "message": message
    }
    return response
