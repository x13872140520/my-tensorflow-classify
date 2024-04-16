import base64
import io
import numpy as np
import requests
import tensorflow as tf
from PIL import Image


def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # 调整图像尺寸
    img_array = np.array(img) / 255.0  # 归一化到 [0, 1] 区间

    return img_array


def predict_with_tf_serving(image_path, server_url='localhost:8501'):
    img_array = preprocess_image(image_path)
    img_array = img_array[np.newaxis, ...]  # 添加批量维度

    # 将图像数据转换为 Base64 编码字符串
    img_bytes = io.BytesIO()
    Image.fromarray(img_array).save(img_bytes, format='PNG')  # 修改这里
    img_b64_str = base64.b64encode(img_bytes.getvalue()).decode()

    # 构建预测请求
    request_data = {
        'signature_name': 'serving_default',
        'instances': [{'input_1': img_b64_str}]
    }

    # 发送预测请求
    response = requests.post(server_url + '/v1/models/mobilenet_flowers2:predict', json=request_data)

    # 解析预测结果
    predictions = response.json()['predictions'][0]
    result_index = np.argmax(predictions)
    return result_index, predictions


if __name__ == '__main__':
    image_path = 'C:/Users/张/Desktop/fix/JPEGImages/1.jpg'  # 替换为您要预测的图像路径
    result_index, probabilities = predict_with_tf_serving(image_path)

    class_names = ['叶子', '李子', '柠檬', '红苹果', '草莓', '西瓜', '西红柿', '青苹果', '香蕉', '黄芒果']  # 替换为您的真实类名列表
    predicted_class = class_names[result_index]

    print(f"Predicted class: {predicted_class}")
    print(f"Probabilities: {probabilities}")