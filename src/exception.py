import sys
import traceback
import logging
from src.logger import logging


def error_message_detail(error, error_detail:sys):
    # Retrieve the exception information (type, value, traceback)
    _,_,exc_tb=error_detail.exc_info()
    # Get the filename where the exception occurred
    file_name =exc_tb.tb_frame.f_code.co_filename
    # Get the line number in the code where the exception occurred
    line_number=exc_tb.tb_lineno
    # Return formatted error message
    error_message = "Error in python script name [{0}] line number [{1}] error message [{2}]".format(
    file_name,line_number,str(error)
    )
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message =error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message 
    
if __name__ == "__main__":
    
    try:
        a =1/0
    except Exception as e:
        logging.info("Division by Zero successful")
        raise CustomException(e,sys)