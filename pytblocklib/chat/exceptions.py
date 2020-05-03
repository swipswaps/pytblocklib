class ChatParseException(Exception):
    '''
    Base exception thrown by the parser
    '''
    pass

class ResponseContextError(ChatParseException):
    '''
    Thrown when chat data is invalid.
    '''
    pass

class NoContents(ChatParseException):
    '''
    Thrown when ContinuationContents is missing in JSON.
    '''
    pass

class NoContinuation(ChatParseException):
    '''
    Thrown when continuation is missing in ContinuationContents.
    '''
    pass

class IllegalFunctionCall(Exception):
    '''
    Thrown when get() is called even though 
    set_callback() has been executed.
    '''
    pass

class InvalidVideoIdException(Exception):
    '''
    Thrown when the video_id is not exist (VideoInfo).
    '''
    pass

class UnknownConnectionError(Exception):
    pass

class RetryExceedMaxCount(Exception):
    '''
    thrown when the number of retries exceeds the maximum value.
    '''
    pass

class ChatDataFinished(ChatParseException):
    pass

class ReceivedUnknownContinuation(ChatParseException):
    pass

class FailedExtractContinuation(ChatDataFinished):
    pass