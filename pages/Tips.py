import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title('Чаевые в ресторане')
st.write("""Загрузи файл _tips.csv_ с данными \n
Скачать данный файл можно по ссылке ниже:
         
https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv""")

@st.cache_data
def upload_etalon_files():
    path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    tips_etalon = pd.read_csv(path)
    return tips_etalon

@st.cache_data
def upload_our_files(etalon, uploaded_file):
    if uploaded_file is not None:
        try:
            tips = pd.read_csv(uploaded_file)
            if etalon.shape == tips.shape:
                st.write('Файл успешно загружен')
                st.write(tips.head(5))
                return tips
            else:
                st.sidebar.write(f'Загружен некорректный файл {uploaded_file.name}')
                st.stop()
        except:
            st.sidebar.write(f'Произошла ошибка при загрузке файла {uploaded_file.name}')
            st.stop()
    else:
        st.stop()

def save_chart(file_name, number):
    if not os.path.exists('save_charts'):
        os.makedirs('save_charts')
    fn = "./save_charts/" + file_name
    plt.savefig(fn)
    with open(fn, 'rb') as img:
        download_button = st.sidebar.download_button(label=f'Скачать график №{number}', 
                    data=img, file_name=file_name)

tips_etalon = upload_etalon_files()
file = st.sidebar.file_uploader('# Загрузи CSV файл', type='csv')
tips = upload_our_files(tips_etalon, file)

start = pd.to_datetime('2023-01-01')
end = pd.to_datetime('2023-01-31')
tips['time_order'] = start + pd.to_timedelta(np.random.randint(0, (end - start).days + 1, size=len(tips)), unit='D')

plot_tips_in_time= tips.groupby(['time_order'])['tip'].sum().reset_index()
plot_tips_in_time_new = plot_tips_in_time.copy()
plot_tips_in_time_new.set_index('time_order', inplace=True)

st.write('### 1. График динамики чаевых во времени')
st.line_chart(plot_tips_in_time_new, x_label='Дата', y_label='Чаевые')
st.write('''
            Данный график является динамически изменяемым,
         поэтому сохранить его вы можете, нажав на него правой кнопкой мышки и выбрав Save image as...\n
         У всех последующих графиков на боковой панели будет кнопка, позволяющая сохранить данный график.''')
st.write('')
fig, ax = plt.subplots()
plot_2 = sns.relplot(data=plot_tips_in_time, x=plot_tips_in_time.index, y='tip', color='r')
plot_2.ax.set_xlabel('Дата')
plot_2.ax.set_ylabel('Чаевые')
st.write('### 2. График динамики чаевых во времени, построенный с помощью многофункционального метода _replot_')
st.pyplot(plot_2)
save_chart('chart_2_tips_in_time_replot.png', 2)

fig_3, ax_3 = plt.subplots()
sns.histplot(tips['total_bill'], ax=ax_3)
st.write('### 3. Гистограмма _total_bill_')
st.pyplot(fig_3)
save_chart('chart_3_hist_total_bill.png', 3)

plot_4 = sns.displot(kind='kde', data=tips, x='total_bill')
st.write('### 4. График, аналогичный предыдущему, построенный с использованием многофункционального метода _displot_')
st.pyplot(plot_4)
save_chart('chart_4_displot_total_bill.png', 4)

fig_5, ax_5 = plt.subplots()
sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax_5)
st.write('### 5. **scatterplot**, показывающий связь между _total_bill_ and _tip_')
st.pyplot(fig_5)
save_chart('chart_5_scatterplot_total_bill.png', 5)

plot_6 = sns.relplot(data=tips, x='total_bill', y='tip', color='purple')
st.write('### 6. График, аналогичный предыдущему, построенный с использованием многофункционального метода _replot_')
st.pyplot(plot_6)
save_chart('chart_6_replot_total_bill.png', 6)

plot_7 = sns.relplot(data=tips, x='total_bill', y='tip', hue='size')
st.write('### 7. График, связывающий _total_bill_, _tip_, и _size_')
st.pyplot(plot_7)
save_chart('chart_7_replot_total_bill_tip_size.png', 7)

fig_8, ax_8 = plt.subplots()
sns.scatterplot(data=tips, x='day', y='total_bill', ax=ax_8)
sns.lineplot(data=tips, x='day', y='total_bill', ax=ax_8)
st.write('### 8. График, показывающий связь между днем недели и размером счета')
st.pyplot(fig_8)
save_chart('chart_8_scatterplot_day_bill.png', 8)

fig_9, ax_9 = plt.subplots()
sns.scatterplot(data=tips, x='tip', y='day', hue='sex', ax=ax_9)
st.write('### 9. _scatter plot_ с днем недели по оси **Y**, чаевыми по оси **X**, и цветом по полу')
st.pyplot(fig_9)
save_chart('chart_9_scatterplot_day_tip_sex.png', 9)

fig_10, ax_10 = plt.subplots()
total_bill_in_time = tips.groupby(['time_order', 'time'])['total_bill'].sum().reset_index()
sns.boxplot(data=total_bill_in_time, x='time', y='total_bill', ax=ax_10)
st.write('### 10. _box plot_ c суммой всех счетов за каждый день, разбитый по _time (Dinner/Lunch)_')
st.pyplot(fig_10)
save_chart('chart_10_boxplot_time_total_bill.png', 10)

plot_11 = sns.catplot(kind='violin', data=total_bill_in_time, x='time', y='total_bill')
st.write('### 11. График, аналогичный предыдущему, построенный с использованием многофункционального метода _catplot_')
st.pyplot(plot_11)
save_chart('chart_11_catplot_time_total_bill.png', 11)

dinner_tips = tips[tips['time'] == 'Dinner'].groupby(['time_order'])['tip'].sum()
lunch_tips = tips[tips['time'] == 'Lunch'].groupby(['time_order'])['tip'].sum()
fig_12, ax_12 = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
sns.histplot(dinner_tips, ax=ax_12[0])
sns.histplot(lunch_tips, ax=ax_12[1])
st.write('### 12. Гистограммы чаевых на обед и ланч')
st.pyplot(fig_12)
save_chart('chart_12_histplot_time_order_tip.png', 12)

df_male = tips[tips['sex'] == 'Male'][['total_bill', 'tip', 'smoker']].reset_index(drop=True)
df_female = tips[tips['sex'] == 'Female'][['total_bill', 'tip', 'smoker']].reset_index(drop=True)
fig_13, ax_13 = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
sns.scatterplot(data=df_male, x='total_bill', y='tip', hue='smoker', ax=ax_13[0])
sns.scatterplot(data=df_female, x='total_bill', y='tip', hue='smoker', ax=ax_13[1])
st.write('### 13. 2 _scatterplots_ (для мужчин и женщин), показавающие связь размера счета и чаевых, разбитые по курящим/некурящим')
st.pyplot(fig_13)
save_chart('chart_13_scatterplots_total_bill_tip_smoker.png', 13)

fig_14, ax_14 = plt.subplots()
sns.heatmap(tips.corr(numeric_only=True), annot=True, fmt='.5g', square=True, ax=ax_14)
st.write('### 14. Тепловая карта зависимостей численных переменных')
st.pyplot(fig_14)
save_chart('chart_14_heatmap_numeric_columns.png', 14)