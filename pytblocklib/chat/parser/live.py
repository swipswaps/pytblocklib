"""
pytchat.parser.live
~~~~~~~~~~~~~~~~~~~
Parser of live chat JSON.
"""

import json
from .. tokenlist import Token
from .. import exceptions

class Parser:
    '''
    Parser parses chatdata JSON and retrieves chat data and metadata such as
    intereval, continuation params, session_token.

    Attributes:
    -----------
        _token : Token
            session token data for operating each chat.
            Token is ssociated with chat id. 
    '''
    #__slots__ = ['is_replay','_token']
    
    def __init__(self, is_replay): 
        self.is_replay = is_replay
        
    def get_contents(self, jsn):
        if jsn is None: 
            raise exceptions.IllegalFunctionCall(
                'Called with None at JSON parameter.')
        if jsn['response']['responseContext'].get('errors'):
            raise exceptions.ResponseContextError(
                'The video_id would be wrong, or video is deleted or private.')
        contents=jsn['response'].get('continuationContents')
        self._tokendict = {"xsrf_token":jsn.get('xsrf_token'), "csn":jsn.get("csn")}
        return contents

    def parse(self, contents):
        """
        Parameter
        ----------
        + contents : dict
            + JSON of chat data from YouTube.

        Returns
        -------
        tuple:
        + metadata : dict
         + timeout
         + video_id
         + continuation           
        + chatdata : List[dict]
        """

        if contents is None:
            '''Broadcasting end or cannot fetch chat stream'''
            raise exceptions.NoContents('Chat data stream is empty.')

        cont = contents['liveChatContinuation']['continuations'][0]
        if cont is None:
            raise exceptions.NoContinuation('No Continuation')
        metadata = (cont.get('invalidationContinuationData')  or
                    cont.get('timedContinuationData')         or
                    cont.get('reloadContinuationData')        or
                    cont.get('liveChatReplayContinuationData')
                    )
        if metadata is None:
            if cont.get("playerSeekContinuationData"):
                raise exceptions.ChatDataFinished('Finished chat data')
            unknown = list(cont.keys())[0]
            if unknown:
                raise exceptions.ReceivedUnknownContinuation(
                    f"Received unknown continuation type:{unknown}")
            else:
                raise exceptions.FailedExtractContinuation(
                    'Cannot extract continuation data')
        return self._create_data(metadata, contents)

    def reload_continuation(self, contents):
        """
        When `seektime = 0` or seektime is abbreviated , 
        check if fetched chat json has no chat data. 
        If so, try to fetch playerSeekContinuationData. 
        This function must be run only first fetching.
        """
        if contents is None:
            '''Broadcasting end or cannot fetch chat stream'''
            raise exceptions.NoContents('Chat data stream is empty.')

        cont = contents['liveChatContinuation']['continuations'][0]
        if cont.get("liveChatReplayContinuationData"):
            #chat data exist.
            return None
        #chat data do not exist, get playerSeekContinuationData.
        init_cont = cont.get("playerSeekContinuationData")
        if init_cont:
            return init_cont.get("continuation")
        raise exceptions.ChatDataFinished('Finished chat data')

    def _create_data(self, metadata, contents):    
        actions = contents['liveChatContinuation'].get('actions')
        if self.is_replay:    
            interval = self._get_interval(actions)
            metadata.setdefault("timeoutMs",interval)
            """Archived chat has different structures than live chat, 
            so make it the same format."""
            chatdata = [action["replayChatItemAction"]["actions"][0]
                for action in actions]
        else:
            chatdata = actions
        metadata.setdefault('timeoutMs', 10000)
        metadata.setdefault('tokendict', self._tokendict)
        return metadata, chatdata

    def _get_interval(self, actions: list):
        if actions is None:
            return 0
        start = int(actions[0]["replayChatItemAction"]["videoOffsetTimeMsec"])
        last = int(actions[-1]["replayChatItemAction"]["videoOffsetTimeMsec"])
        return (last - start)