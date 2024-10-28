import os
import cv2
import matplotlib.pyplot as plt

# 数据集路径
dataset_path = 'DOTA-v1.5_val'
image_folder = os.path.join(dataset_path, 'images')  # 假设图像存放在images文件夹中
label_folder = os.path.join(dataset_path, 'labels')  # 假设标签存放在labels文件夹中


def convert_to_yolo_format(label_file, img_width, img_height):
    yolo_lines = []
    with open(label_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # 跳过无效行
        if not line or 'gsd:' in line:
            continue

        # 尝试解析边界框信息
        parts = line.split()
        if len(parts) < 6:  # 至少需要类ID和四个坐标
            continue

        class_name = parts[-2]  # 类名在倒数第二个位置
        class_id = int(parts[-1])  # 类ID在最后一个位置

        try:
            # 提取多边形坐标
            coords = list(map(float, parts[:-2]))  # 除去类名和类ID后剩余的都是坐标

            # 计算边界框的最小外接矩形
            x_min = min(coords[0::2])
            y_min = min(coords[1::2])
            x_max = max(coords[0::2])
            y_max = max(coords[1::2])

            # 计算中心坐标和宽高
            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height

            yolo_lines.append(f"{class_id} {x_center} {y_center} {width} {height}\n")
        except ValueError as e:
            print(f"Error processing line: '{line}'. Error: {e}")

    return yolo_lines


# 可视化每个图像及其对应的标签
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        image_name = label_file.replace('.txt', '.png')  # 假设图像为jpg格式
        image_path = os.path.join(image_folder, image_name)

        # 读取图像
        image = cv2.imread(image_path)
        h, w, _ = image.shape

        # 读取标签并绘制边界框
        with open(os.path.join(label_folder, label_file), 'r') as f:
            for line in f.readlines():
                line = line.strip()

                if not line or 'gsd:' in line:
                    continue

                parts = line.split()
                if len(parts) < 6:
                    continue

                class_id = int(parts[-1])  # 类ID在最后一个位置

                try:
                    coords = list(map(float, parts[:-2]))  # 除去类名和类ID后剩余的都是坐标

                    # 计算边界框的最小外接矩形
                    x_min = min(coords[0::2])
                    y_min = min(coords[1::2])
                    x_max = max(coords[0::2])
                    y_max = max(coords[1::2])

                    # 将YOLO格式转换为边界框坐标
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2

                    x1 = int((x_center) * w)
                    y1 = int((y_center) * h)
                    x2 = int((x_max) * w)
                    y2 = int((y_max) * h)

                    # 绘制边界框
                    cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (255, 0, 0), 2)

                except ValueError as e:
                    print(f"Error processing line: '{line}'. Error: {e}")

        # 显示图像
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(image_name)
        plt.show()

# 转换所有标签文件并保存为YOLO格式
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        original_label_path = os.path.join(label_folder, label_file)

        # 获取对应图像的尺寸（假设已知或可通过其他方式获取）
        img_width = ...  # 替换为实际图像宽度
        img_height = ...  # 替换为实际图像高度

        yolo_annotations = convert_to_yolo_format(original_label_path, img_width, img_height)

        # 保存为新的YOLO格式文件
        new_label_path = original_label_path.replace('labels', 'yolo_labels')  # 假设保存到yolo_labels文件夹中
        with open(new_label_path, 'w') as f:
            f.writelines(yolo_annotations)