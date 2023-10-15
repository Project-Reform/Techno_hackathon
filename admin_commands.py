import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import matplotlib.pyplot as plt

async def createExcelFileReportCommand(startDate,endDate,users):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    df = pd.DataFrame(columns=['user_id'])
    date_start = datetime.strptime(startDate, "%Y%m%d")
    date_end = datetime.strptime(endDate, "%Y%m%d")
    days = []
    current_date = date_start

    while current_date <= date_end:
        days.append(str(current_date.date()).replace('-', ''))
        current_date += timedelta(days=1)
    for i, user in enumerate(users):
        df.loc[i, 'user_id'] = user
        for j, day in enumerate(days):
            cur_waterHabit.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='waterDates' AND sql LIKE '%date_{day}%'")
            if cur_waterHabit.fetchone() is not None:
                answer = cur_waterHabit.execute(f"SELECT date_{day} FROM waterDates WHERE user_id = ?", (user,)).fetchone()
                answer = answer[0]
            else:
                answer = 'No data'
            date_obj = datetime.strptime(day, '%Y%m%d')
            date_formatted = date_obj.strftime('%d:%m:%Y')
            df.loc[i, str(date_formatted)] = answer if answer else None
    db_waterHabit.close()
    df.to_excel('userData.xlsx', index=False)


async def createExcelFileActionCommand(startDate,endDate,users):
    db_user_interactions = sqlite3.connect('Databases/user_interactions.db')
    cur = db_user_interactions.cursor()
    workbook = Workbook()
    print(startDate, endDate)
    for user in users:
        df = pd.DataFrame(columns=['action', 'time'])
        results = cur.execute("SELECT action, time FROM users WHERE user_id = ?", (user,)).fetchall()
        print(results)
        for result in results:
            dateTimeStartDate = datetime.strptime(startDate, '%d:%m:%Y')
            dateTimeEndDate = datetime.strptime(endDate, '%d:%m:%Y')
            resultDateTime = datetime.strptime(result[1][0:10], '%Y-%m-%d')
            if dateTimeStartDate <= resultDateTime <= dateTimeEndDate:
                new_df =  pd.DataFrame([(result[0], result[1])], columns=['action', 'time'])
                df = pd.concat([df,new_df], ignore_index=True)
        sheet = workbook.create_sheet(title=user)
        for row in dataframe_to_rows(df, index=False, header=True):
            sheet.append(row)
    workbook.remove(workbook['Sheet'])
    workbook.save('getUserAction.xlsx')


async def createGraphReportCommand(dateStart,user_id):
    dateEnd = datetime.now().date()
    dateStart = dateStart.date()
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cursor = db_waterHabit.cursor()
    delta = dateEnd - dateStart
    all_dates = []
    plotColumns = []
    plotRows = []
    cursor.execute("PRAGMA table_info(waterDates)")
    columns = cursor.fetchall()
    for i in range(delta.days + 1):
        current_date = dateStart + timedelta(days=i)
        current_date = 'date_' + str(current_date).replace('-', '')
        all_dates.append(current_date)

    for column in columns:
        if column[1] in all_dates:
            plotColumns.append(column[1])
            userAction = cursor.execute(f"SELECT {column[1]} FROM waterDates WHERE user_id = ?",(user_id,)).fetchone()
            plotRows.append(userAction[0])
    for i, date_string in enumerate(plotColumns):
        year = int(date_string[5:9])
        month = int(date_string[9:11])
        day = int(date_string[11:13])
        date_string_formatted = f"{day:02}:{month:02}:{year}"
        plotColumns[i] = date_string_formatted
    print(plotRows)
    for i in range(len(plotRows)):
        if plotRows[i] == 'y':
            plotRows[i] = 1
        else:
            plotRows[i] = 0
    plt.plot(plotColumns, plotRows)
    plt.yticks([0, 1])
    plt.xlabel('Дата')
    plt.ylabel('Получилось ли выполнить привычку')
    plt.title('Ваш график по привычке питьё воды')

    plt.savefig('scatter_plot.png')

