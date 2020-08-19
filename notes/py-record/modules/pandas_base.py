import pandas as pd
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

print(data.info())  # 显示每一列的数据类型，及其中是否为空
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
