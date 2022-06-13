from email import header
import streamlit as st
import pandas as pd
from io import StringIO as stringio
import csv
import os
import time
import numpy as np
from scipy.interpolate import interp1d

#查询函数
def query_data(df, param1, param2, param3):
    return ((df[param1]>param2)&(df[param1]<param3))

#缺失值补全函数
def fillna(data, param):
    tmp_X = data[param].values
    X = np.array(range(len(tmp_X)))
    tmp_X_NA = tmp_X[np.where(np.isnan(tmp_X)!=1)]
    X_0 = X[np.where(np.isnan(tmp_X) != 1)]
    IRFunction = interp1d(X_0, tmp_X_NA, kind = 'linear')
    Fill_X = X[np.where(np.isnan(tmp_X) == 1)]
    Fill_Y = IRFunction(Fill_X)
    tmp_X[Fill_X] = Fill_Y 
    return (tmp_X)

logfilepath = 'C:/Users/BLUE/Desktop/研一/课程/数据库/NCAA2022/log.txt'
datafiledir = 'C:/Users/BLUE/Desktop/研一/课程/数据库/NCAA2022/'
st.markdown('DATABASE EASYUSE')

st.title('数据库管理系统')

# 1.创建
st.subheader('新建数据表')
filename = st.text_input('please input filename with file extensions:')
if st.button('New File'):
    if filename is not None:
        with open(datafiledir+filename,'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X","Y","Z","W"])
            st.write(filename +' has been created')
        with open(logfilepath,'a+') as logfile:
            logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+filename+'>>>create datagraph\n')
        #st.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+filename+'>>>create datagraph')
# 2 打开
st.subheader('打开数据表')
uploaded_file = st.file_uploader("Choose a file... csv")
if uploaded_file is not None:
     dataframe = pd.read_csv(uploaded_file)
     st.write(dataframe)
     with open(logfilepath,'a+') as logfile:
        logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+uploaded_file.name+'>>>open datagraph\n')
     #st.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+uploaded_file.name+'>>>open datagraph')
# 2.修改
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
with col1:
    st.subheader('更新数据表')
    pa1 = st.number_input('X')
    pa2 = st.number_input('Y')
    pa3 = st.number_input('Z')
    pa4 = st.number_input('W')
    if st.button('Update'):
        with open(datafiledir+uploaded_file.name,'r',newline='') as file_up:
            reader = csv.reader(file_up)
            header = next(reader)
            data = list(reader)
        row_contents = [pa1, pa2, pa3, pa4]
        data.append(row_contents)
        with open(datafiledir+uploaded_file.name,'w',newline='') as file_up:
            writer = csv.writer(file_up)
            writer.writerow(header)
            writer.writerows(data)
        updateframe = pd.read_csv(datafiledir+uploaded_file.name)
        st.write(updateframe)
        with open(logfilepath,'a+') as logfile:
            logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+uploaded_file.name+'>>>update datagraph\n')
# 4.管理
with col3:
    st.subheader('管理数据表')
    if st.button('ShowDir'):
        dir = "C:/Users/BLUE/Desktop/研一/课程/数据库/NCAA2022"
        for root, dirs, files in os.walk(dir):
            for name in files:
                st.write(name)
# 5.查询
with col2:
    st.subheader('查询数据表')
    p1 = st.text_input('X,Y,Z,W')
    p2 = st.number_input('min')
    p3 = st.number_input('max')
    if st.button('Query'):
        csv_dfQ = dataframe.loc[query_data(dataframe, param1=p1, param2=p2, param3=p3), :]
        st.write(csv_dfQ)
        with open(logfilepath,'a+') as logfile:
            logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+uploaded_file.name+'>>>query datagraph\n')
#6日志
#7.数据补全
with col4:
    st.subheader('缺失值补全')
    if st.button('Fillna'):
        dataframe['X']=fillna(dataframe, 'X')
        dataframe['Y']=fillna(dataframe, 'Y')
        dataframe['Z']=fillna(dataframe, 'Z')
        dataframe['W']=fillna(dataframe, 'W')
        st.write(dataframe)
        s = uploaded_file.name
        res = s.split('.')
        dataframe.to_csv(datafiledir+res[0]+'-cahche.csv', index=False)
        with open(logfilepath,'a+') as logfile:
            logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+uploaded_file.name+'>>>fillna datagraph\n')
st.subheader('保存数据表')
savefilename = st.text_input('filename')
st.write(savefilename)
if st.button('Save'):
    s = uploaded_file.name
    res = s.split('.')
    os.rename(datafiledir+res[0]+'-cahche.csv',datafiledir+savefilename)
    st.write(savefilename +' has been saved')
    with open(logfilepath,'a+') as logfile:
            logfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'   '+savefilename+'>>>save file\n')