import datetime
from typing import Union

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from src.services.firebase.firebase import ServiceFirebase
from src.services.mailchimp.mailchimp import MailChimpService
from src.services.minio.minio_client import MinioClient
from src.services.redis.redis_client import RedisClient
from src.services.worker.worker import ServiceWorker


class BaseController:
    def __init__(
            self,
            request: Request = None,
            service_worker: ServiceWorker = None,
            redis_client: RedisClient = None,
            current_user: Union[dict, None] = None,
            minio_client: MinioClient = None,
            mailchimp_client: MailChimpService = None,
            firebase_client: ServiceFirebase = None
    ):
        self.errors = []
        self.transaction_start_time = datetime.datetime.now()
        self.host_of_client_call_request = request.client.host
        self.request = request
        self.service_worker = service_worker
        self.redis_client = redis_client
        self.current_user = current_user
        self.minio_client = minio_client
        self.mailchimp_client = mailchimp_client
        self.firebase_client = firebase_client

    def response_openai_chat(self, data, status_code=HTTP_200_OK):
        response = JSONResponse(
            content=data,
            status_code=status_code
        )
        return response
    
    def response(
            self,
            data='',
            error_description: str = '',
            status_code: int = HTTP_200_OK,
            extra_data: dict = None
    ):
        response_data = {
            'data': data,
            'errors': self.errors,
            'error_description': error_description,
            'start_time': str(self.transaction_start_time),
            'end_time': str(datetime.datetime.now()),
            'host_of_client_call_request': self.host_of_client_call_request,
            'total_time_by_second': (datetime.datetime.now() - self.transaction_start_time).total_seconds(),
            'status': 'success' if status_code == HTTP_200_OK else 'failed'
        }
        if extra_data:
            response_data.update(extra_data)
        try:
            response = JSONResponse(
                content=response_data,
                status_code=status_code
            )
        except Exception as e:
            response_data['errors'].append(
                {
                    'loc': 'BaseController',
                    'msg': e.__class__.__name__,
                    'detail': str(e)
                }
            )
            response_data['status'] = 'failed'
            response = JSONResponse(
                content={
                    'data': None,
                    'errors': self.errors,
                    'error_description': error_description
                },
                status_code=HTTP_400_BAD_REQUEST
            )
        return response
