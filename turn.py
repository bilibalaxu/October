import os

# 数据集路径
dataset_path = 'DOTA-v1.5_val'
label_folder = os.path.join(dataset_path, 'labels')  # 原始标签文件夹
yolo_label_folder = os.path.join(dataset_path, 'yolo_labels')  # YOLO格式标签保存文件夹

# 创建YOLO标签保存文件夹（如果不存在）
os.makedirs(yolo_label_folder, exist_ok=True)


def convert_to_yolo_format(label_file, img_width, img_height):
    yolo_lines = []
    with open(label_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # 跳过无效行
        if not line or 'gsd:' in line:
            continue

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


# 遍历所有标签文件并转换为YOLO格式
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        original_label_path = os.path.join(label_folder, label_file)

        # 假设图像的宽度和高度已知，替换为实际值
        img_width = 1024  # 替换为实际图像宽度
        img_height = 1024  # 替换为实际图像高度

        yolo_annotations = convert_to_yolo_format(original_label_path, img_width, img_height)

        # 保存为新的YOLO格式文件，使用 .yolo 后缀
        new_label_path = os.path.join(yolo_label_folder, label_file.replace('.txt', '.yolo'))
        with open(new_label_path, 'w') as f:
            f.writelines(yolo_annotations)

print("转换完成，YOLO格式文件已保存。")