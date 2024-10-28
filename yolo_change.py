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