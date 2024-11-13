import numpy as np
import matplotlib.pyplot as plt

# 读取数据
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip()]
    return data

# 主程序
if __name__ == '__main__':
    file_path = '../data_pictures/110.txt'  # 请将此处更改为您的 txt 文件路径
    data = read_data_from_file(file_path)
    reference = 110
 
    # 计算统计信息
    max_value = np.max(data)
    min_value = np.min(data)
    mean_value = np.mean(data)
    variance = np.var(data)

    # 假设我们有一个函数计算 precision 和 accuracy
    # 这里为了示例，我们用随机值代替真实的计算
    precision = (max_value-min_value)/2  # 假设的 precision 值
    accuracy =  abs(mean_value-reference)   # 假设的 accuracy 值

    # 绘制点图
    plt.figure(figsize=(10, 6))
    plt.plot(data, 'o', label='Data Points')
    plt.title('Data Points with Statistics')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid()

    # 在右上角标记统计信息
    stats_text = (f'Max: {max_value:.5f}\n'
                f'Min: {min_value:.5f}\n'
                f'Mean: {mean_value:.5f}\n'
                f'Variance: {variance:.5f}\n'
                f'Precision: {precision:.5f}\n'
                f'Accuracy: {accuracy:.5f}')

    plt.text(0.95, 0.25, stats_text, transform=plt.gca().transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(facecolor='white', alpha=0.5))

    plt.legend()
    plt.show()

