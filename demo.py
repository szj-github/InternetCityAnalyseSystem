import os

# 保存不同模型的目录名(绝对路径)
file_dir = r'E:\untitled\map'

for root, dirs, files in os.walk(file_dir):
    for filename in files:
        name, ext = os.path.splitext(filename)
        if name in '广州省':
            print(name)

