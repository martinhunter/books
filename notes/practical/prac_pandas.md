import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def preset(filename):
	suffix = filename.endswith
	if suffix('.csv'):
		# csv使用`,`作为分隔符
		read_file = pd.read_csv
		to_file = pd.DataFrame.to_csv
	elif suffix('.xls') or suffix('.xlsx'):
		read_file = pd.read_excel
		to_file = pd.DataFrame.to_excel
	else:
		raise NameError("the filename is not recognizable")

	return read_file,to_file

sep = lambda e='': print('---',e,'end -----------')
filename = 'md.csv'
read_file,to_file = preset(filename)


# %start
data = read_file(filename)

# print(data.info())  # 显示每一列的数据类型，及其中是否为空
# sep()
# print(data['one'].describe())  # 会自动计算平均数等
# sep()
# print(data.agg({'one': ['min', 'max', 'median', 'skew'],
# 				'two': ['min', 'max', 'median', 'mean']}) 
# 		) # describe特定的计算，agg 是aggregate
# print(data.dtypes)  # 显示数据类型
# sep()

'''
数据的第一行会作为筛选行,filter_row
其余可称为数据行,data_row
data[<elem_of_filter_row>]
'''
fa = data['one']  # 筛选出第一个名称为one的列
f2 = data['two']  # 筛选出第一个名称为one的列
fi = data[['two','four']]  # 筛选出第一行名称为two,four的列


# print(fi.head(2))  # 默认获取前5行，不含筛选行
# sep("head")

# print(data.head(2))  # 获取前2行，不含筛选行
# sep("tail")


# above = data[fa > 6]  # 若fa中元素有字符串，则会报错
# print('bigger than',above.head())
# sep()

# inside = data[f2.isin(['one',22])]  # f2的数据行中元素符合['one',6],选出此行
# print('Is in v1:')
# print(inside)
# sep()

# inside = data[fi.isin(['one',22])]  # 对多列使用则会显示所有数据行
# print('Is in v2:')
# print(inside)
# sep()

# inside = data[f2.isin(['one',22]) | data['four'].isin(['one',22])]  # 每次删选一列并用|,&,!组合以显示所需行
# print('Is in v3:')
# print(inside)
# sep()

# not_null = data[data["three"].notna()]
# print("--not null--", not_null.head())
# sep()

# above_filtered = data.loc[8, "three"]  # 显示第8行，列'three'的内容
# print(above_filtered.head())
# sep()

# above_filtered = data.loc[fa > 6, "three"]  # 仅显示特定列'three'的内容
# print(above_filtered.head())
# sep()

# data['add_filter'] = data['two'] + "added"  # 添加新列
# print(data.head())
# sep()

# print(data.iloc[4:8, 2:5])  # 选择特定区域,4-7行，2-4列

# data.iloc[4:8, 2] = 'newValue'  # 为特定区域设置值
# print(data.iloc[4:8, 2])
# sep()


# # quickmath
# print("type:", type(data['one']))
# print(data['one'].mean())
# sep('mean')

# # groupby([filt_1st,filt_2ed]) 可进行多项分组
# data[["sex", "one"]].groupby("sex").mean()  # 用sex分组，one列对每个分组求平均值,只显示sex,one 2列

# data.groupby("sex")['one'].mean()  # 作用同上，但计算步骤会多一步
# sep("groupby")

# print(data['two'].value_counts())  # 记录每个值出现的次数,titanic.groupby("Pclass")["Pclass"].count()简写而来
# sep("count times")

# # adjust shape

# print(data.sort_values(by=['first', 'one'], 
# ascending=False).head())  # 全都递减，第一个条件排序完，再尝试排序第二个条件
# sep('sort')

# no2 = data[data["sex"] == "female"]  # data中符合条件的行
# print(no2.head())
# sep('filt sex first')

# no2_subset = no2.sort_index().groupby("gob").head(3)
# print(no2_subset)
# sep("subset")

# print(no2_subset.pivot(columns="two", values="one"))  # 将two列设置为column


# to_file(data, filename, index=None)


# practical part
# NOTE: 1个列表应只存储同一个类型的数据
# NOTE: 对Series对象的处理都生成一个新对象，而不修改原Series对象

original_li = [10,11,12,14]
ds = pd.Series(original_li)
another_li = [24,26,28,30]
ds2 = pd.Series(another_li)

[link](https://www.w3resource.com/python-exercises/pandas/python-pandas-data-series-exercise-33.php)
# Series转换为列表
retrive_li = ds.tolist()

# 两个Series可用+-*/等基本操作符进行操作
mixed_ds = ds * ds2

# 可直接转换字典
original_dict = {'a': 100, 'b': 200, 'c':300, 'd':400, 'e':800}
dicts = pd.Series(original_dict)

# 可直接转换narray
np_array = np.array([10, 20, 30, 40, 50])
nar = pd.Series(np_array)

# 对Series对象,显式强制类型转换(为float64),不符合要求的值会转换为NaN
s1 = pd.Series(['100', '200', 'python', '300.12', '400'])
s2 = pd.to_numeric(s1, errors='coerce')

# 字典的键转换为DataFrame的列名
d = {'col1': [1, 2, 3, 4, 7, 11], 'col2': [4, 5, 6, 9, 5, 0], 'col3': [7, 5, 8, 12, 1,11]}
df = pd.DataFrame(data=d)
# s1 = df.ix[:,0]  # ???

# 使用s1.values对值复制,并将这些值保存在一个numpy.ndarray对象中
s1 = pd.Series(['100', '200', 'python', '300.12', '400'])
# print("Original Data Series:")
# ndarr = s1.values

# 将内部的多个列表合为一个列表
s = pd.Series([
    ['Red', 'Green', 'White'],
    ['Red', 'Black'],
    ['Yellow']])
s = s.apply(pd.Series).stack().reset_index(drop=True)

# 重新排序
s = pd.Series([80, 20, 6, 30, 40, 50])
ordered_s = pd.Series(s).sort_values()
sr2 = pd.Series([20,40])

# 将不同的列进行合并
new_s = s.append(pd.Series([10, 5]))

# 筛选值
# Series同list,可用 s[n1:n2] 取值
# 也可用 s[SeriesObj] ,此SeriesObj保存True,False值,且长度要与s相同
n = 35
ltn_s = s[s < n]
ltn_s2 = s[pd.Series([True, True,False,False,True,True])]
not_ins = s[~s.isin(sr2)]  # 用~取反,等同sr1.notin(sr2)
range_s = s[:3]

# 筛选值并获取其index
# result = np.argwhere(s)  可能报错，不知道是不是版本问题

# (极少使用) 用reindex完全控制排序,Series中默认index = list(range(n))
s = pd.Series([1,2,3,4,5], index = ['A', 'B', 'C','D','E'])
s = s.reindex(index = ['B','A','C','D','E'])
first_val = s.index[2]  # Series.index[n]可获得index列中的值
print(first_val == 'C')

# Series的sum,average,mean计算
s.mean()
s.std()

# 使用np.union1d,np.intersect1d进行集合操作
# NOTE：会去除重复值
sr1 = pd.Series([1, 2, 3, 4, 5])
sr2 = pd.Series([2, 4, 6, 8, 10])
sr11 = pd.Series(np.union1d(sr1, sr2))
sr22 = pd.Series(np.intersect1d(sr1, sr2))

# np.percentile获取Series中的最小值，中间的值等
num_state = np.random.RandomState(100)
num_series = pd.Series(num_state.normal(10, 4, 20))
result = np.percentile(num_series, q=[0, 25, 50, 75, 100])

# 元素计数
# 将num_series中值的集合设为result的index，index的值为它出现的次数。并按出现次数从高到低排列
num_series = pd.Series(np.take(list('0123456789'), np.random.randint(10, size=40)))
result = num_series.value_counts()  
# num_series.value_counts().index[:1]获取第一个index
result2 = num_series[~num_series.isin(result.index[:1])] = 'Other'

# 获取特定index处的值
num_series = pd.Series(list(range(100,150)))
element_index = [0, 2, 6, 11, 21]
result = num_series.take(element_index)

# 获取特定值的index（不宜用于有重复数据的Series）
# pd.Index(series1).get_loc(i)
# 找到series1中i值所在的index
series1 = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
series2 = pd.Series([1, 3, 5, 7, 10])
result = [pd.Index(series1).get_loc(i) for i in series2]


# map处理单个元素
series1 = pd.Series(['one','two'])
result = series1.map(lambda x: x[0].upper() + x[1:-1] + x[-1].upper())

# diff()获得前后元素的差值，用于数字
series2.diff().tolist()

# 自动转换时间字符串为同一规格
date_series = pd.Series(['01 Jan 2015', '10-02-2016', '20180307', '2014/05/06', '2016-04-12', '2019-04-06T11:20'])

date_series_1 = pd.to_datetime(date_series)  # 方法1

from dateutil.parser import parse  # 方法2
date_series_2 = date_series.map(lambda x: parse(x))

# 获取年月日
date_series_2.dt.day.tolist()
date_series_2.dt.dayofyear.tolist()
date_series_2.dt.weekofyear.tolist()
# date_series_2.dt.weekday_name.tolist() weekday_name似乎不同版本名字不同

# 欧几里得度量,对(x-y)的平方和进行开根号
x = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = pd.Series([11, 8, 7, 5, 6, 5, 3, 4, 7, 1])
np.linalg.norm(x-y)

import pandas as pd
import numpy as np
nums = pd.Series([1, 8, 7, 5, 6, 5, 3, 4, 7, 1])

# np.sign(s)会将s中的正数转换为1，负数转换为-1,a<b为正数
first_part = np.sign(np.diff(nums))
# >>> [ 1 -1 -1  1 -1 -1  1  1 -1]
comp_prev = np.where(temp == 1)[0] + 1  # 与前数相比，因此需+1
comp_next = np.where(temp == -1)[0]  # 与后数相比，不+1

# 若第二次也不+1，数的index为s[n],它与s[n+1],s[n+2]进行比较


temp = np.diff(np.sign(np.diff(nums)))
# a<b,b<c,return 0
# a>b,b>c,return 0
# a<b,b>c,return -2
# a>b,b<c,return 2
print(temp)
result = np.where(temp == -2)[0] + 1  # 第二次与前数相比，因此需+1，数的index为s[n],它与s[n-1],s[n+1]进行比较
print(result)
