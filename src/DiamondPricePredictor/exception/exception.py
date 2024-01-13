import sys


class CustomException(Exception):
    def __init__(self, error_msg, error_details: sys):
        self.error_msg = str(error_msg)
        _,_,exc_tb = error_details.exc_info()
        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in the python script -> [{self.file_name}] on the line number -> [{self.line_no}] with the error message -> [{self.error_msg}]"

    
if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        raise CustomException(e,sys)