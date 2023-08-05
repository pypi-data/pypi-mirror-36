"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Dict
from .client import _Client


class ActionClient(_Client):
    """
    A client for the Cortex Actions API.
    """

    URIs = {
        'deploy': 'actions',
        'invoke': 'actions/{action_name}/invoke',
        'logs': 'actions/{action_name}/logs',
        'status': 'actions/{action_name}/status',
        'delete': 'actions/{action_name}',
        'task_logs': 'jobs/{action_name}/tasks/{task_id}/logs',
        'task_status': 'jobs/{action_name}/tasks/{task_id}/status'
    }

    def deploy_action(self, name: str, kind: str, docker: str, code: str = '', action_type: str = None, **kwargs):
        """
        Deploy an Action.

        :param name: the resource name of the Action
        :param kind: the Action kind (only for  functions) - python:2, python:3
        :param docker: the Docker image to use (optional for functions, required for jobs and daemons)
        :param code: the Action code to deploy.  Expects a file-like object and zip compressed contents.
        :param action_type: The type of action workload: function, daemon, job (Default: function)
        :return:
        """
        action = {'name': name}

        if docker:
            action['docker'] = docker

        if kind:
            action['kind'] = kind

        if code:
            try:
                code_file = open(code, 'rb')
            except TypeError:
                code_file = code

            action['code'] = ('code.zip', code_file, 'application/zip')

        if kwargs.get('command'):
            action['command'] = kwargs.get('command')

        if kwargs.get('port'):
            action['port'] = kwargs.get('port')

        if kwargs.get('environment'):
            action['environment'] = kwargs.get('environment')

        if kwargs.get('vcpus'):
            action['vcpus'] = kwargs.get('vcpus')

        if kwargs.get('memory'):
            action['memory'] = kwargs.get('memory')

        uri = self.URIs['deploy']
        if action_type is not None:
            uri = '{}?actionType={}'.format(uri, action_type)

        m = MultipartEncoder(action)
        r = self._serviceconnector.request(method='POST', uri=uri, body=m, headers={'Content-type': m.content_type})
        r.raise_for_status()
        return r.json()

    def invoke_action(self, action_name, params: Dict[str, object]) -> Dict[str, object]:
        """
        Invoke an Action.

        :param action_name: the name of the Action to invoke
        :param params: the body params to send the Action

        :return: the result of calling the Action
        """
        uri = self.URIs['invoke'].format(action_name=action_name)
        return self._post_json(uri, params)

    def get_logs(self, action_name) -> Dict[str, object]:
        """
        Get the most recent logs for an Action

        :param action_name: the Action name to retrieve logs for

        :return: the most recent logs for the requested Action
        """
        uri = self.URIs['logs'].format(action_name=action_name)
        return self._get_json(uri)

    def delete_action(self, action_name, action_type=None):
        """
        Delete an Action.
        :param action_name: the name of the Action to delete
        :return:
        """
        uri = self.URIs['delete'].format(action_name=action_name)
        if action_type:
            uri = '{}?actionType={}'.format(uri, action_type)

        r = self._serviceconnector.request(method='DELETE', uri=uri)
        r.raise_for_status()

        return r.json()

    def get_task_status(self, action_name, task_id):
        """
        Get the status for an Action Task (for Job type Actions only)

        :param action_name:
        :param task_id:
        :return:
        """
        uri = self.URIs['task_status'].format(action_name=action_name, task_id=task_id)
        r = self._serviceconnector.request(method='GET', uri=uri)
        r.raise_for_status()

        print(r.raw)
        return r.text


    def get_task_logs(self, action_name, task_id):
        """
        Get the logs for an Action Task (for Job type Actions only)

        :param action_name:
        :param task_id:
        :return:
        """
        uri = self.URIs['task_logs'].format(action_name=action_name, task_id=task_id)
        return self._get_json(uri)
