import util

data = [[(1, 4), 3], [(1, 5), 4], [(2, 1), 1], [(3, 1), 2], [(4, 1), 3], [(4, 4), 6], [(5, 1), 4],
        [(7, 4), 9], [(10, 4), 12], [(13, 4), 15], [(13, 5), 16], [(14, 5), 17]]

# 使用 min() 函数找到第二个值最小的一项，并获取其下标
min_index, min_item = min(enumerate(data), key=lambda x: x[1][1])

print("列表中第二个值最小的一项：", min_item)
print("其所在列表在整个大列表中的下标：", min_index)
