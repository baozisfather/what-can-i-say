import requests
import base64
import cv2 as cv


# opencv 图片
def vehicle_detect(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image)
    params = {"image":base64_image}
    access_token = '24.d5c555413e33fbd581ba73a52cf6c00e.2592000.1722670981.282335-90614977'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    num = 0
    if response:
        data = response.json()
        num = data['vehicle_num']['car']
        for item in data['vehicle_info']:
            location = item['location']
            x1 = location['left']
            y1 = location['top']
            x2 = x1 + location['width']
            y2 = y1 + location['height']
            cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
        # 定义要绘制的文字
            text = item['type']
            position = (x1, y1-2)
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            color = (0, 0, 255)  # 红色
            thickness = 2
            img = cv.putText(img, text, position, font, font_scale, color, thickness, cv.LINE_AA)
            # cv.imshow('Rectangle', img)
            # return img
    return img, num




import cv2 as cv
import base64
import requests

def vehicle_moduel(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"
    _, encoded_image = cv.imencode('.jpg', img)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')  # 将 Base64 编码的图像转换为字符串
    params = {"image": base64_image}
    access_token = '24.d5c555413e33fbd581ba73a52cf6c00e.2592000.1722670981.282335-90614977'
    request_url = f"{request_url}?access_token={access_token}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)

    vehicle_data = []

    if response and response.status_code == 200:
        data = response.json()
        if 'result' in data and 'car' in data['result']:
            for item in data['result']['car']:
                vehicle_data.append({
                    "type": item.get('type', 'Unknown'),
                    "color": item.get('color', 'Unknown'),
                    "year": item.get('year', 'Unknown'),
                })
        else:
            print("未找到车辆数据:", data)
    else:
        print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")

    return img, vehicle_data

