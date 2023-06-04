import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import scipy.stats as stats


def preprocess_data(dataframe):
    data = dataframe[dataframe.columns[0]].str.split(pat = ',', expand = True)
    data.columns = ['num_sick_day', 'age', 'sex']
    data.num_sick_day = pd.to_numeric(data.num_sick_day)
    data.age = pd.to_numeric(data.age)
    data.sex = data.sex.apply({'"М"': 1, '"Ж"': 0}.get)
    return data

def first_descriptions(df: pd.DataFrame, column) -> None:
    """Displays some dataset description like:
    * head of dataset
    * info(generated by pandas)
    * categorical features uniques
    * dublicates
    * NaN's
    Args:
        df (pd.DataFrame): DataFrame
    """

    column.write('***Dublicate check***')
    column.write(f"Number of dublicates is : {df.duplicated().sum()}")

    column.write('***NaN check***')
    column.write(f"Total number of NaN is : {df.isna().sum().sum()}")
    column.write(f"Number of NaN by column  : \n {df.isna().sum()}")

@st.cache_data()
def plot_distribution(data, feature_name, bins=10, kde=True):
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    sns.histplot(
        data=data,
        x=feature_name,
        bins=bins,
        ax=ax,
        kde=kde,   
    )
    ax.set_title(f"Распределение признака {feature_name}")
    return fig

def main():
    # ------------------- Переменные -------------------
    uploaded_file = None
    df_raw = None

    # ------------------- Начальные настройки -------------------
    st.set_page_config()
    
    # Загрузка файла и все что с ним связано 
    st.header("Загрузка файлов")
    st.write("Загрузите csv файл со следующей структурой: ")
    st.dataframe(pd.DataFrame({'"Количество больничных дней","Возраст","Пол"': ['5,25,"М"', '5,25,"М"','5,25,"М"', '5,25,"М"', '5,25,"М"']}))
    uploaded_file = st.file_uploader("Choose a file", type='csv')
    if uploaded_file is not None: # Если пользователь ввел файл
        # Читаем
        df_raw = pd.read_csv(uploaded_file, encoding="Windows-1251")
    else:
        # Если нет - кидаем ошибку
        st.warning("you need to upload a csv file.")
        return
    
    # Если не прочитали файл - выходим
    if df_raw is None:
        return
    
    st.header("Обработка данных")
    # ------------------- Смотрим на то как обработали таблицы -------------------
    # Дальше выводим данные из таблиц, 1 - "сырая", вторая - обработанная
    df_column_raw, df_column_processed, info_column = st.columns(3)

    df_column_raw.title("Raw data")
    df_column_raw.dataframe(df_raw)

    data = preprocess_data(df_raw)
    df_column_processed.title("Processed data")
    df_column_processed.dataframe(data)

    info_column.title("Info")
    first_descriptions(data, info_column)

    # ------------------- Графики -------------------
    # Обычнае распределения
    st.header("Распределения признаков")
    fig1 = plot_distribution(data, 'num_sick_day', bins=9, kde=True)
    fig2 = plot_distribution(data, 'age', kde=True)
    fig3 = plot_distribution(data, 'sex', bins=2, kde=False)
    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)


    # Зависимости
    st.header("Распределения признаков в зависимости друг от друга")
    st.subheader("От пола")

    sex_depend_work_day_col, sex_depend_age_col = st.columns(2)
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.histplot(
        data=data,
        x='num_sick_day',
        hue='sex',
        stat='count',
        element='bars',
        kde=True,
        ax=ax,
        bins=data.num_sick_day.max() + 1
    )
    sex_depend_work_day_col.write('Распределение числа больничных дней')
    sex_depend_work_day_col.pyplot(fig)
    sex_depend_work_day_col.write("Основные статистики")
    sex_depend_work_day_col.dataframe(data.groupby('sex')['num_sick_day'].describe())


    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.histplot(
        data=data,
        x='age',
        hue='sex',
        stat='count',
        element='bars',
        kde=True,
        ax=ax
    )
    sex_depend_age_col.write('Распределение возраста')
    sex_depend_age_col.pyplot(fig)
    sex_depend_age_col.write("Основные статистики")
    sex_depend_age_col.dataframe(data.groupby('sex')['age'].describe())

    
    # Скрипки
    st.subheader("Те же зависимости, но в виде скрипичного графика")

    sex_depend_work_day_col, sex_depend_age_col = st.columns(2)
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.violinplot(
        data=data,
        x='sex',
        y='num_sick_day',
        ax=ax,
    )
    sex_depend_work_day_col.write('Распределение числа больничных дней')
    sex_depend_work_day_col.pyplot(fig)
    sex_depend_work_day_col.write("Основные статистики")
    sex_depend_work_day_col.dataframe(data.groupby('sex')['num_sick_day'].describe())


    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.violinplot(
        data=data,
        x='sex',
        y='age',
        ax=ax,
    )
    sex_depend_age_col.write('Распределение возраста')
    sex_depend_age_col.pyplot(fig)
    sex_depend_age_col.write("Основные статистики")
    sex_depend_age_col.dataframe(data.groupby('sex')['age'].describe())

    # Зависимости возраста и 
    st.subheader("Зависимость числа больничных дней и возраста")
    g = sns.JointGrid(data=data, x="age", y="num_sick_day", marginal_ticks=True)
    cax = g.figure.add_axes([1, 0.2, .05, .6])
    g.plot_joint(
        sns.histplot, 
        discrete=(True, True), 
        cbar=True, 
        cbar_ax=cax, 
        cmap=sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True)
    )
    g.plot_marginals(sns.histplot, element="step");
    st.pyplot(g.figure)

    # Матрица корреляций
    st.subheader("Матрица корреляций")
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    sns.heatmap(data.corr(), annot=True, ax=ax)
    st.pyplot(fig, clear_figure=True)

    # ------------------- Гипотезы -------------------
    st.header("Гипотезы")
    inp_days, inp_age = st.columns(2)
    work_day = inp_days.number_input("work_day", min_value=0, max_value=data.num_sick_day.max(), value=int(data.num_sick_day.mean()))
    age = inp_age.number_input("age", min_value=0, max_value=data.age.max(), value=int(data.age.mean()))
    alpha=0.05

    # Гипотеза 1	
    # Эти write'ы  нужно переделать, я пока не нашел решения
    st.write("# Гипотеза 1	")
    st.write(f"Мужчины пропускают в течение года более {work_day} рабочих дней (work_days) по болезни значимо чаще женщин. ")
    st.write("## Решение:  ")
    st.write("1) Формулируем гипотезы  ")
    st.write(fr"$H_0 : $ Нет разницы между мужчинами и женщинами, которые пропустили более {work_day}х рабочих дней  ")
    st.write(fr"$H_1 : $ Разница между мужчинами и женщинами есть")
    st.write("2) Выберем уровень значимости  ")
    st.write(fr"**Пусть $\alpha = {alpha}$**  ")
    st.write("3) Выберем, какой тест будем использовать")
    st.write("Использовать будем критерий согласия Пирсона, так как нужно проверить соответствие наблюдаемых частот с теоретическими. Переформулируем гипотезы: " )
    st.write(fr"$H_0 : $ Частота пропуска {work_day}х и более дней для женщин такая же как и у мужчин  ")
    st.write(fr"$H_1 : $ Частота пропуска {work_day}х и более дней для женщин не такая как у мужчин ")
    st.write(r"Ожидаемые частоты вычислим следующим образом: $$\nu^{Ж(М)}_{>{work_day}} = n_{Ж(М)}\frac{n_{>work_day}}{N}$$, где $n_{Ж(М)}$ - число женщин (мужчин) в выборке, $n_{>work_day}$ - число работников, которые пропустили больше work_day дней, $N$ - размер выборки ")

    # Посмотрим, какая ожидаемая частота была бы, если верна 0-я гипотеза
    frequency = data.query(f'num_sick_day > {work_day}').shape[0] / data.shape[0]
    st.metric(f"Ожидаемая доля, пропустивших более {work_day} дней для мужин и женщин если верна $H_0$  :", value=frequency)
    # Теперь сформируем массив с ожидаемой и наблюдаемой частотой
    # Ожидаемая
    expected = np.array([
        frequency * data.query('sex == 1').shape[0],
        frequency * data.query('sex == 0').shape[0]
    ])
    st.write("Ожидаемое число")
    men_col, wom_col = st.columns(2)
    men_col.metric(label=f"Мужчин, пропустившие более {work_day} дней", value=expected.tolist()[0])
    wom_col.metric(label=f"Женщин, пропустившие более {work_day} дней", value=expected.tolist()[1])
    # Наблюдаемая
    observed = np.array([
        data.query(f'sex == 1 & num_sick_day > {work_day}').shape[0],
        data.query(f'sex == 0 & num_sick_day > {work_day}').shape[0],
    ])
    st.write("Наблюдаемое число")
    men_col, wom_col = st.columns(2)
    men_col.metric(label=f"Мужчин, пропустившие более {work_day} дней", value=observed.tolist()[0])
    wom_col.metric(label=f"Женщин, пропустившие более {work_day} дней", value=observed.tolist()[1])

    # Тест
    test_result = stats.chisquare(f_obs=observed, f_exp=expected)
    st.subheader("Результат теста: ")
    result_stat_col, result_p_col = st.columns(2)
    result_stat_col.metric(label=f"Статистика", value=test_result.statistic)
    result_p_col.metric(label=f"p_value", value=test_result.pvalue)
    st.metric(label=r'Уровень значимости $\alpha$', value=alpha)
    st.write("***ОТВЕРГАЕМ $H_0$***" if test_result.pvalue < alpha else "***НЕ ОТВЕРГАЕМ $H_0$***")

    # Гипотеза 2
    # Эти write'ы  нужно переделать, я пока не нашел решения
    st.write("# Гипотеза 2")
    st.write(f"Работники старше {age} лет (age) пропускают в течение года более {work_day} рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.")  
    st.write("## Решение:  ")
    st.write("1) Формулируем гипотезы  ")
    st.write(fr"$H_0 : $ Нет разницы между работниками $>{age}$ и $\le{age}$ лет, которые пропустили более {work_day}х рабочих дней  ")
    st.write(fr"$H_1 : $ Разница между работниками, которые пропустили более {work_day}х рабочих дней возрастом $> {age}$ и $\le{age}$ есть")
    st.write("2) Выберем уровень значимости  ")
    st.write(r"**Пусть $\alpha = 0.05$**  ")
    st.write("3) Выберем, какой тест будем использовать")
    st.write("Использовать будем критерий согласия Пирсона, так как нужно проверить соответствие наблюдаемых частот с теоретическими. Переформулируем гипотезы:  ")
    st.write(fr"$H_0 : $ Частота пропуска {work_day}х и более дней для работника $>{age}$ лет такая же как и у работника $\le{age}$ лет  ")
    st.write(fr"$H_1 : $ Частота пропуска {work_day}х и более дней для работника $>{age}$ лет не такая же как и у работника $\le{age}$ лет  ")
    st.write("Ожидаемое количество рассчитаем аналогично Гипотезе 1")
    # Посмотрим, какая ожидаемая частота была бы, если верна 0-я гипотеза
    frequency = data.query(f'num_sick_day > {work_day}').shape[0] / data.shape[0]
    st.metric(f"Ожидаемая доля, пропустивших более {work_day} дней для работника $>{age}$ и у работника $\le{age}$ лет если верна $H_0$ :", value=frequency)
    # Теперь сформируем массив с ожидаемой и наблюдаемой частотой
    # Ожидаемая
    expected = np.array([
        frequency * data.query(f'age > {age}').shape[0],
        frequency * data.query(f'age <= {age}').shape[0]
    ])
    st.write("Ожидаемое число")
    greater_col, le_col = st.columns(2)
    greater_col.metric(label=fr"Людей, $>$ {age}, пропустившие более {work_day} дней", value=expected.tolist()[0])
    le_col.metric(label=fr"Людей, $\le$ {age}, пропустившие более {work_day} дней", value=expected.tolist()[1])
    # Наблюдаемая
    observed = np.array([
        data.query(f'age > {age} & num_sick_day > {work_day}').shape[0],
        data.query(f'age <= {age} & num_sick_day > {work_day}').shape[0],
    ])
    st.write("Наблюдаемое число")
    greater_col, le_col = st.columns(2)
    greater_col.metric(label=f"Люди $>$ {age}, пропустившие более {work_day} дней", value=observed.tolist()[0])
    le_col.metric(label=f"Люди $\le$ {age}, пропустившие более {work_day} дней", value=observed.tolist()[1])
    # Тест    
    test_result = stats.chisquare(f_obs=observed, f_exp=expected)
    st.subheader("Результат теста: ")
    result_stat_col, result_p_col = st.columns(2)
    result_stat_col.metric(label=f"Статистика", value=test_result.statistic)
    result_p_col.metric(label=f"p_value", value=test_result.pvalue)
    st.metric(label=r'Уровень значимости $\alpha$', value=alpha)
    st.write("***ОТВЕРГАЕМ $H_0$***" if test_result.pvalue < 0.05 else "***НЕ ОТВЕРГАЕМ $H_0$***")



if __name__=='__main__':
    main()