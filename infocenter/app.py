from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/post', methods=['POST'])
def handle_post():
    try:
        # 获取请求的时间
        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取请求的 URL
        request_url = request.url
        # 获取请求头信息
        request_headers = dict(request.headers)
        # 获取请求体内容
        request_body = request.get_json()

        if request_body is None:
            raise ValueError("Invalid JSON data")

        # 记录日志
        logging.info(f"Request Time: {request_time}")
        logging.info(f"Request URL: {request_url}")
        logging.info(f"Request Headers: {request_headers}")
        logging.info(f"Request Body: {request_body}")

        # 返回成功响应
        return jsonify({"status": "success", "message": "Request received and logged"}), 200

    except Exception as e:
        # 记录异常日志
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)