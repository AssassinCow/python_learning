import numpy as np

arr1 = np.array([1, 2, 3])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
arr3 = np.ones(4)
arr4 = np.array([13, 2, 6])

print(arr1.ndim)
print(arr2.ndim)

print(arr1.shape)
print(arr2.shape)

print(arr1.size)
print(arr2.size)

print(np.concatenate([arr1,arr3]))

print(arr1+arr4)
print(arr1*3)

print(arr4[(arr4>=6) & (arr4<13)])