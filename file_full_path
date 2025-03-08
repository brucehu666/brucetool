import unittest
import json
from flask import Flask
from app import app  # 更新导入路径

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # 设置测试客户端
        self.app = app.test_client()
        self.app.testing = True

    def test_post_request(self):
        # 测试 POST 请求
        data = {
            "key1": "value1",
            "key2": "value2"
        }
        response = self.app.post('/post', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Request received and logged')

    def test_post_request_with_no_json(self):
        # 测试 POST 请求，不包含 JSON 数据
        response = self.app.post('/post', data='not json', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Request received and logged')

    def test_post_request_with_invalid_json(self):
        # 测试 POST 请求，包含无效 JSON 数据
        response = self.app.post('/post', data='{invalid json}', content_type='application/json')
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'error')

if __name__ == '__main__':
    unittest.main()