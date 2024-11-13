import numpy as np
import sys
import os


def process_ranges(ranges):
    # 标记异常值：将 ranges 中为 0 的值标记为异常
    abnormal_indices = np.where(ranges == 0)[0]
    print(f"异常值的索引: {abnormal_indices}")

    # 对 ranges 做差分并取绝对值
    diff_abs = np.abs(np.diff(ranges))

    # 创建一个字典来存储差分值和对应的索引
    diff_dict = {i: diff_abs[i] for i in range(len(diff_abs))}
    
    # 按照差分值排序字典（从大到小）
    sorted_diff_dict = {k: v for k, v in sorted(diff_dict.items(), key=lambda item: item[1], reverse=True)}

    # 获取最大的几个差分值及其索引
    num_largest = 5  # 要找的最大数个数
    largest_indices_sorted = list(sorted_diff_dict.keys())[:num_largest]
    
    print(f"最大差分值的索引: {largest_indices_sorted}")
    print(f"最大差分值: {[sorted_diff_dict[i] for i in largest_indices_sorted]}")

def read_ranges_from_file(file_path):
    with open(file_path, 'r') as file:
        # 读取文件中的所有数值，假设每行一个数
        data = np.loadtxt(file,max_rows=360)

    # 只处理第一组数据（前360个数）
    ranges = data[:360]
    if len(ranges) == 360:
        process_ranges(ranges)

if __name__ == '__main__':
    # 获取当前脚本的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # 构建相对于脚本所在目录的文件路径
    file_path = os.path.join(current_directory, 'laser_ranges.txt')

    # 处理文件中的前360个数据
    read_ranges_from_file(file_path)
