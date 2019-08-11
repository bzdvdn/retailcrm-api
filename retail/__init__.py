import json
import requests
from time import sleep
from urllib.parse import urlencode


class RetailAPIException(Exception):
    def __init__(self, status, message, *args, **kwargs):
        self.status = status
        self.message = message
        super().__init__(args, kwargs)
    

    def __str__(self):
        return f"Status: {self.status}, message: {self.message}"


class RetailSession(object):
    POST_METHODS = [
        "fix_external_ids", "create", "edit", "combine",
        "delete", "links", "event","upload","update_invoice", "status"
    ]


    def __init__(self, crm_url, api_token, version='v5'):
        self.crm_url = f"{crm_url[:-1]}/api/{version}/" if crm_url.endswith("/") else f"{crm_url}/api/{version}/"
        self.api_token = api_token
        self.requests_session = requests.Session()


    def _send_api_request(self, url, params, http_method):
        if http_method == 'post':
            response = self.requests_session.post(url, data=params, headers={
                "Content-type": "application/x-www-form-urlencoded"
            })
        else:
            url += "&" + urlencode(params)
            response = self.requests_session.get(url)
        try:
            data = response.json()
            success = data.pop("success", False)
            pagination = data.pop("pagination", {})
            generated_at = data.pop("generatedAt", None)
            result_name = next(iter(data))
            if not success:
                raise RetailAPIException(422, data)

            total_pages = pagination.get("totalPageCount", 1)
            result_data = data[result_name]
            if total_pages > 1:
                for page in range(2,total_pages+1):
                    url += f"&page={page}"
                    response = self.requests_session.get(url).json()
                    sleep(0.3)
                    result_data.extend(response[result_name])
                    
            return result_data
        except json.JSONDecodeError:
            raise RetailAPIException(406, f"bad requests, {response.text}")



    def send_api_request(self, request, object_id, params):
        if object_id:
            path = "/".join(p for p in request.methods[:-1])
            url = f"{self.crm_url}{path}/{object_id}/{request.methods[-1]}"
        else:
            path = "/".join(p for p in request.methods)
            url = f"{self.crm_url}{path}"
        
        url = f"{url}?apiKey={self.api_token}"
        params = params or {}
        http_method = "post" if request.methods[-1] in self.POST_METHODS else "get"  
        return self._send_api_request(url, params, http_method)



class RetailAPI(object):
    def __init__(self, crm_url, api_token, timeout=60, headers={}, version='v5'):
        self._session = RetailSession(crm_url, api_token, version=version)
        self._timeout = timeout
        self._method_default_headers = headers


    def __getattr__(self, method_name):
        return Request(self, method_name)


    def __call__(self, method_name, **method_kwargs):
        return getattr(self, method_name)(**method_kwargs)


class Request(object):
    __slots__ = ('_api', '_method_args', "methods")


    def __init__(self, api, method_or_methods):
        self._api = api
        self.methods = []
        if isinstance(method_or_methods, list):
            self.methods.extend(method_or_methods)
        else:
            self.methods.append(method_or_methods)


    def __getattr__(self, method_or_methods):
        if isinstance(method_or_methods, list):
            self.methods.extend(method_or_methods)
        else:
            self.methods.append(method_or_methods)
        return Request(self._api, self.methods)


    def __call__(self, object_id=None, params=None, **method_args):
        self._method_args = method_args
        return self._api._session.send_api_request(self, object_id, params)