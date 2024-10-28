from ultralytics import YOLO

# 加载YOLOv11模型
model = YOLO('yolo11n.pt')  # 使用预训练的YOLOv11权重

# 定义训练参数
train_params = {
    'data': 'yolo_labels/dataset.yolo',  # 数据集配置文件路径
    'epochs': 50,                         # 训练轮数
    'imgsz': 640,                         # 输入图像大小
    'batch': 16,                          # 批量大小
    'device': 'cpu',                        # 使用的GPU设备，'0'表示第一个GPU，'cpu'表示使用CPU
}

# 开始训练
results = model.train(**train_params)

# 保存最终训练权重
model.save('yolov11_final_weights.pt')