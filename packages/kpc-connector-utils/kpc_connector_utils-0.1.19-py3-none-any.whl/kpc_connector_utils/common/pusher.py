from kpc_connector_utils.common.types import EventType
from kpc_connector_utils.common.context_wrapper import ContextWrapper
from kpc_connector_utils.common.base64 import base64_encode

import json
import boto3


class Pusher:
    def __init__(self, config):
        self._config = config

    def push_event(self, custom_context: dict = None):
        ct_wrapper = ContextWrapper()

        custom_client_context = ct_wrapper.create_custom_client_context()
        if custom_context:
            if not custom_client_context.get('custom'):
                custom_client_context['custom'] = {}

            for k, v in custom_context.items():
                custom_client_context['custom'][k] = v

        lambda_client = boto3.client('lambda')
        if self._config.event_type == EventType.Event:
            lambda_client.invoke(FunctionName=self._config.func_name,
                                 InvocationType=self._config.event_type,
                                 LogType='None',
                                 ClientContext=base64_encode(json.dumps(custom_client_context)),
                                 Payload=self._config.__str__().encode())

        elif self._config.event_type == EventType.RequestResponse:
            return lambda_client.invoke(FunctionName=self._config.func_name,
                                        InvocationType=self._config.event_type,
                                        LogType='None',
                                        ClientContext=base64_encode(json.dumps(custom_client_context)),
                                        Payload=self._config.__str__().encode())

        else:
            raise ValueError('Not specify event type or it is not available')
