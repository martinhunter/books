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
#                 'two': ['min', 'max', 'median', 'mean']}) 
#         ) # describe特定的计算，agg 是aggregate
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














# MARK:practical part






# phase 1. Series:是最基本的结构。相当于1列（但实际上是2列，另一列为隐藏的index列）
# NOTE: 每次Series对象的处理都会生成（返回）一个新对象，而不修改原Series对象
# NOTE: 1个Series只应存储同一个类型的数据

original_li = [10,11,12,14]
ds = pd.Series(original_li)
another_li = [24,26,28,30]
ds2 = pd.Series(another_li)

# Series转换为列表
retrive_li = ds.tolist()

# 两个Series可用+-*/等基本操作符进行操作，
# S.apply(func)对每个元素应用func,部分情况可与map互换，但apply应用范围更广
# 还有特殊操作符S.isnull(),S.notnull(),S.between(12,30),&,|,S.sum()S.mean(),S.std()
mixed_ds = ds * ds2

# 可直接转换字典,`abcde`会作为index,100,200等作为Series的值
original_dict = {'a': 100, 'b': 200, 'c':300, 'd':400, 'e':800}
dicts = pd.Series(original_dict)

# 可直接转换np.array
np_array = np.array([10, 20, 30, 40, 50])
nar = pd.Series(np_array)
# print(nar.values)

# to_numeric强制类型转换(为float64),不符合要求的值会转换为NaN
s1 = pd.Series(['100', '200', 'python', '300.12', '400'])
s2 = pd.to_numeric(s1, errors='coerce')

# 使用s1.values获得值,并将这些值保存在一个numpy.ndarray对象中
s1 = pd.Series(['100', '200', 'python', '300.12', '400'])
ndarr = s1.values

# 将内部的多个列表合为一个列表
s = pd.Series([
    ['Red', 'Green', 'White'],
    ['Red', 'Black'],
    ['Yellow']])
s = s.apply(pd.Series).stack().reset_index(drop=True)

# 重新排序
s = pd.Series([80, 20, 10, 30, 40, 50])
ordered_s = pd.Series(s).sort_values()  # 2种皆可
ordered_s2 = s.sort_values()

# 将不同的列进行合并
new_s = s.append(pd.Series([10, 5]))

# 筛选值
# Series可用 s[n1:n2] 取值
# 也可用 s[SeriesObj],根据SeriesObj值为True,False,且长度要与s相同
ranges = s[1:3]
big_s = s[s > 33]  # s<33返回一个对象pd.Series([True,False,False,False,True,True]
# NOTE: 返回对象的长度（即元素数量）需与s相等
sr2 = pd.Series([21,41])
not_ins = s[~s.isin(sr2)]  # 用~取反,等同sr1.notin(sr2)

# 筛选值并获取其index
# result = np.argwhere(s>20)  # 报错或不报错，不知道是不是版本问题

# 使用S.index获得index
# (极少使用) 用reindex完全控制排序,Series中默认index = list(range(n))
s = pd.Series([13,2,3,4,5], index = ['A', 'B', 'C','D','E'])
s = s.reindex(index = ['B','A','C','D','E'])
current_index = s.index
first_three_index = s.index[:2]
biggest_index = s.idxmax()  # 获取最大最小值对应的index
smallest_index = s.idxmin()
biggest_index2 = s.values.argmax()  # 获取最大值对应的index

# 获取特定index处的值
num_series = pd.Series(list(range(100,150)))
element_index = [0, 2, 6, 11, 21]
result = num_series.take(element_index)

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
# num_series.value_counts().index[:1]获取列表（不然不能用isin）
result2 = num_series[~num_series.isin(result.index[:1])] = 'Other'

# map处理每个元素
series1 = pd.Series(['one','two'])
result = series1.map(lambda x: x[0].upper() + x[1:-1] + x[-1].upper())

# 直接修改所有某类型的数据
up = series1.str.upper()
low = series1.str.lower()
get_len = series1.str.len()
get_striped = series1.str.strip()


# 自动转换时间字符串为同一规格
date_series = pd.Series(['01 Jan 2015', '10-02-2016', '20180307', '2014/05/06', '2016-04-12', '2019-04-06T11:20'])
date_series_1 = pd.to_datetime(date_series)  # 方法1
from dateutil.parser import parse  # 方法2
date_series_2 = date_series.map(lambda x: parse(x))

# 获取年月日
date_series_2.dt.day.tolist()
date_series_2.dt.dayofyear.tolist()
date_series_2.dt.isocalendar().week.tolist()
# date_series_2.dt.weekday_name.tolist() weekday_name似乎不同版本名字不同

# 欧几里得度量,对(x-y)的平方和进行开根号
x = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = pd.Series([11, 8, 7, 5, 6, 5, 3, 4, 7, 1])
np.linalg.norm(x-y)

# diff()获得前后元素的差值，用于数字
y.diff().tolist()

# 获取比右左边都大数的index
nums = pd.Series([1, 8, 7, 5, 6, 5, 3, 4, 7, 1])
# np.sign(s)会将s中的正数转换为1，负数转换为-1,a<b为正数
temp = np.sign(np.diff(nums))
# >>> [ 1 -1 -1  1 -1 -1  1  1 -1]
comp_prev = np.where(temp == 1)[0] + 1  # 与前数相比，因此需+1。where返回([0, 3, 6, 7], dtype=int32),用[0]取[0, 3, 6, 7]
comp_next = np.where(temp == -1)[0]  # 与后数相比，不+1
# 若第二次也不+1，数的index为s[n],它与s[n+1],s[n+2]进行比较
temp = np.diff(np.sign(np.diff(nums)))
# a<b,b<c,return 0
# a>b,b>c,return 0
# a<b,b>c,return -2
# a>b,b<c,return 2
result = np.where(temp == -2)[0] + 1  # 第二次与前数相比，因此需+1，数的index为s[n],它与s[n-1],s[n+1]进行比较

# 获取值的位置
se = pd.Series(data=[10,12,12,12,13,13,15,12,13],index=['one','three','five','nine','thee','fve','ne','aae','five'])
result = se.value_counts()
match_index = se.index.get_loc("five")  # se.index匹配index列。
# get_loc的结构可能类似这样
class series:
    def __init__(self,data=None,index=None):

    # data和index会经过处理
        # ommited
        self.values = data
        self.index = index if index else range(len(data))
        # ommited
    def get_loc(self, val):
        temp = []
        counter = 0
        cur = 0
        for i in range(len(self.values)):
            if self[i] == val:
                temp[i] = True
                counter += 1
                cur = i
            else:
                temp[i] = False
        if counter == 0:
            raise KeyError(19)
        elif counter == 1:
            return cur
        else:
            return np.array(temp)
match_value = pd.Index(se).get_loc(13)  # pd.Index(se)匹配data列。
match_value2 = np.array(se == 13)  # 效果相同

# 检测自相关
num_series = pd.Series(np.arange(15) + np.random.normal(1, 10, 15))
autocorrelations = [num_series.autocorr(i).round(2) for i in range(11)]
# print(autocorrelations[1:])

# 获取当前年份的所有星期天
result = pd.Series(pd.date_range('2020-01-01', periods=52, freq='W-SUN'))




# phase 2. DataFrame：由1或多个Series构成

# 配置pandas。columns不包括index列
# 超范围后则只显示第一和最后，中间所有行或列都只用一列或一行...表示
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# 性能解析,显示内存使用情况
df = pd.DataFrame({
    'Name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Eesha Hinton', 'Syed Wharton'],
    'Date_Of_Birth ': ['17/05/2002','16/02/1999','25/09/1998','11/05/2002','15/09/1997'],
    'Age': [18.5, 21.2, 22.5, 22, 23]
})
# df.info(memory_usage = "deep")  # 会自动打印
memo_of_each_col = df.memory_usage(deep = True)

# 多个Series合并为一个dataFrame的3种方式
series1 = pd.Series(range(10,20))
series2 = pd.Series(list('pqrstuvwxy'))

df_concat = pd.concat([series1, series2], axis=1)
df_direct = pd.DataFrame(series1, series2).reset_index()
df_dict = pd.DataFrame({"col1":series1, "col2":series2})

# numpy array 创建
dtype = [('Column1','int32'), ('Column2','float32'), ('Column3','float32')]
values = np.zeros(15, dtype=dtype)
index = ['Index'+str(i) for i in range(1, len(values)+1)]
ndf = pd.DataFrame(values, index=index)

# 内部为多个列表创建
my_lists = [['col1', 'col2'], [2, 4], [1, 3], [5, 6]]
# sets the headers as list
headers = my_lists.pop(0)
df = pd.DataFrame(my_lists, columns = headers)

# 字典的键转换为DataFrame的列名,每个列名对应一个SeriesObj
# NOTE：index列是隐藏的，没有列名
exam_data  = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
        'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
        'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
df = pd.DataFrame(data=exam_data, index=labels)  # index也可自动生成
col_types = df.dtypes

# 读取
first3 = df.head(3)  # 获取前3行
last3 = df.tail(3)  # 获取最后3行
df1 = df.nlargest(3, 'score')  # 获取score列前3的行
filtered_df = df.select_dtypes(include = "number")  # 筛选特定类型的列
# loc,at必须列名和index名
# iloc,iat则用数字代表列名和index名
# loc可获取多行多列，at则获取特定单元格，都是行在前，列在后
filter_rows = df[ df['score']>13 ]  # 筛选行,df['col2'>5]返回SeriesObj
first2 = df.iloc[:1]  # iloc筛选行
choose_cells = df.iloc[[1,3,8], [1,2]]  # iloc筛选行，列
choose_cell = df.at['e', 'score']
filter_cell = df.loc['a'].at['score']

ss2 = df['score']
column1and3 = df[['attempts','name']]  # 根据列名筛选特定列,并将attempts列放前边
indexes = df.axes[0]  # 返回index列
col_names = df.axes[1]  # 返回所有列的名称
the_index = df.index  # 返回index列
index2to4 = df.index[[2,4]]  # 获取2和4处的索引
col_names2 = df.columns  # 返回所有列的名称
col_index = df.columns.get_loc("score")  # 返回特定列的索引
ss1 = df.score  # 获取特定名字的列，2者作用相同

list(col_names.values)  # 通过.values获得对象存储的值
count_nan = df.isnull().values.sum()  # 获取nan的总个数
string = df.to_string(index=False)    # 表转化为string，除了index

# 写入（不写入index）和读取
df.to_csv('new_file.csv', sep='\t', index=False)
new_df = pd.read_csv('new_file.csv')

# 修改
df =  df.fillna(0)  # 将所有nan替换为0
df = df.reset_index()  # index部分转换为名叫index的列，使用默认的range(n)作为index。drop=True则删除原有index，使用默认的range(n)
df = df.set_index('index')  # 将index列转换为index
prefix_df = df.add_prefix("A_")  # 添加前后缀
suffixed_df = df.add_suffix("_1")
df.columns = df.columns.str.lower().str.rstrip()  # 修改列名

df.reset_index(level=0, inplace=True)  # inplace不生成新对象，直接将index部分转换为名叫index的列
df = df.set_index('index')

df.loc['d', 'score'] = 11.5  # 设置值
df.at['e', 'score'] = 10.2  # 设置值
df.iat[8, 1] = 12  # 设置值,i为integer
df.loc['k'] = ['Suresh', 15.5,1,'yes']  # 添加新行，k为index
df = df.drop('k')  # 根据index删除行，drop不生成新的DataFrame对象，也可drop index对象
df2 = {'name': "newbody", 'score': 11, 'attempts': 2}
df = df.append(df2, ignore_index=True)  # append添加新行
df['color'] = ['Red','Blue','Orange','Red','White','White','Blue','Green','Green','Red','cyan']  # 添加新列
df.pop('color')  # 删除列

df.score = df.score.astype(int)  # 强制类型转化为int类型
new_col = range(11)
df.insert(loc=0, column='col1', value=new_col)  # 插入至特定位置
df['name'] = df['name'].replace('James', 'Suresh')  # replace替换
df['name'] = df['name'].replace('[A-Z]{1,2}ames', 'Suresh', regex=True)  # 正则替换
df = df.replace([9,20], 15)  # 将所有cell中的9或20改为15
df = df.replace([10,20], [15,16])  # 将所有cell中的10改为15,20改为16
new_df = df.append(ndf)  # 使用append添加其他DataFrame,类似full outer join。效果如下
dd = pd.DataFrame({"name":['a b c','d e f','g h i',' j k l','m n']})
dd[["first", "middle", "last"]] = dd["name"].str.split(" ", expand = True)
print(dd)

"""
df = pd.DataFrame({"col12": range(4),"col4": range(4)})
data = pd.DataFrame({"col1": range(3),"col2": range(3)})
print("After appending some data:")
df = df.append(data,sort=True)
print(df)
After appending some data:
   col1  col12  col2  col4
0   NaN    0.0   NaN   0.0
1   NaN    1.0   NaN   1.0
2   NaN    2.0   NaN   2.0
3   NaN    3.0   NaN   3.0
0   0.0    NaN   0.0   NaN
1   1.0    NaN   1.0   NaN
2   2.0    NaN   2.0   NaN

df = pd.DataFrame({"col2": range(4),"col4": range(4)})
data = pd.DataFrame({"col1": range(3),"col2": range(3)})
print("After appending some data:")
df = df.append(data,sort=True)
print(df)

After appending some data:
   col1  col2  col4
0   NaN     0   0.0
1   NaN     1   1.0
2   NaN     2   2.0
3   NaN     3   3.0
0   0.0     0   NaN
1   1.0     1   NaN
2   2.0     2   NaN
"""

# NOTE:loc和pop,df['name']=对df进行了修改而不是生成一个新的对象

# TODO：检查merge的作用
df1 = df.copy(deep = True)  # 深度拷贝
df = df.drop([0, 1])
df1 = df1.drop([2])
df_one_to_one = pd.merge(df, df1, validate = "one_to_one")

# 排序
ordered_sort = df.sort_values(by=['name', 'score'], ascending=[True, True])
# 随机取样
sample_df = df.sample(frac=1)  # frac=0.3则取30%的行

# 分组
# 1. groupby(["attempts"])获得分组后的对象,"attempts"的值集合和"score"的值集合再次集合，成为新index
# .size()获得每组的出现次数的df
# reset_index将Series转换为DataFrame
g1 = df.groupby(["attempts","score"]).size()  # 返回Series对象
g1 = df.groupby(["attempts","score"]).size().reset_index(name='Number of attempts')
g1 = df.groupby("attempts").size().reset_index(name='Number of attempts')
# 将每个attempts组的所有score组成一个list作为值。返回Series对象
other_cols = df.groupby('attempts')['score'].apply(list)

# map的特殊用法,将yes改为True,no改为False
df['qualify'] = df['qualify'].map({'yes': True, 'no': False})

# 另一种传入的结构，列表中的每个字典都是1行
exam_data = [{'name':'Anastasia', 'score':12.5}, {'name':'Dima','score':9}, {'name':'Katherine','score':16.5}]
df = pd.DataFrame(exam_data)
# 遍历
for index, row in df.iterrows():
    cur_name = row['name']
    cur_score = row['score']


# 重命名列
d = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
df = pd.DataFrame(data=d)
# 方法1（长度必须match）
df.columns = ['Column1', 'Column2', 'Column3']
df = df.rename(columns={})
# 方法2（长度可不match，而只改特定column）
df = df.rename(columns={'col1': 'Column1', 'col3': 'Column3'})


# 比较df和sr每行值是否相等
df_data = pd.DataFrame({'W':[68,75,86,80,None],'X':[78,75,None,80,86], 'Y':[84,94,89,86,86],'Z':[86,97,96,72,83]});
sr_data = pd.Series([68, 75, 86, 80, None])
bool_df = df_data.ne(sr_data, axis = 0)

# 通过to_frame将index也转化为1个Series
char_list = list('ABCDEFGHIJKLMNOP')
num_arra = np.arange(8)
num_dict = dict(zip(char_list, num_arra))
num_ser = pd.Series(num_dict)
df = num_ser.to_frame()
df = num_ser.to_frame().reset_index()


# 进行范围判断并重映射（类似map）
df = pd.DataFrame({
    'name': ['Alberto Franco','Gino Mcneill','Ryan Parkes', 'Gino Mcneill', 'Syed Wharton', 'Kierra Gentry'],
      'age': [18, 22, 85, 0, 80, 5]
})
# df["age"]中的值符合 0<= and <=18映射为"kids", <18 and <=65映射为"adult", <65 and <=99映射为"elderly"
df["age_groups"] = pd.cut(df["age"], bins = [0, 18, 65, 99], labels = ["kids", "adult", "elderly"])


# 随机表生成器
df1 = pd.util.testing.makeDataFrame() # index为字母数字组成的随机值
df2 = pd.util.testing.makeMissingDataframe() # index为字母数字组成的随机值，且col中有空值
df3 = pd.util.testing.makeTimeDataFrame() # index为日期对象
df4 = pd.util.testing.makeMixedDataFrame() # col为随机类型（同一列的值为同类型）
date_series = pd.util.testing.makeDateIndex()[0:6]  # 生成6个时间对象

# interpolate会根据其他值，推测nan处的可能值并填充
sdata = {"c1":[120, 130 ,140, 150, np.nan, 170], "c2":[7, 10, 7, np.nan, 5.5, 16.5]}
missed_df = pd.DataFrame(sdata)
interpolated_df = missed_df.interpolate()

# 模拟查询语句筛选行
maxx = interpolated_df["c1"].max()
queried_df = missed_df.query("c1 < @maxx")

# 用不同数字表示不同的值，相同值用同一个数字
label1, unique1 = pd.factorize(missed_df['c2'])

# S.cummax()效果同cmax。
df1=pd.DataFrame({'rnum':[23, 21, 27, 22, 34, 33, 34, 31, 25, 22, 36, 19, 31, 32, 19]})
df1.rnum.cummax()
def cmax(li):
    curMax = 0
    new_li = []
    # 遍历，若当前值cur小于当前的最大值cmax，则将cur设置为cmax
    for i in li:
        if i >= curMax:
            curMax = i
        new_li.append(curMax)
    return new_li

# False处改为10，而True的不变
where_df = df1.rnum.where([True, False, True, False, True, False, True, False, False, False, True, False, False, False, False],10)

# 读取剪切板
read_df = pd.read_clipboard()

# 比较不同的值
df1 = pd.DataFrame({'W':[68,75,86,80,None]});
df2 = pd.DataFrame({'W':[78,75,82,80,None]})
where_1_not_equal_2 = df1.ne(df2)

# 获取c1列值最小的3行
df1 = missed_df.nsmallest(3, 'c1')
