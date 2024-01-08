import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s[A-Za-z]+\]\s'
    mess = re.split(pattern, data)[1:]
    dates_1 = re.findall(pattern, data)
    dates_wo_bracket = []
    user = []
    message = []
    datetime_n = []
    for i in dates_1:
        dates_wo_bracket.append(i.replace("[", "").replace("]", "").replace('\u202f', ' ').strip())
    df = pd.DataFrame({'user_message': mess, 'message_date': dates_wo_bracket})

    for datetime_str in df['message_date']:
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%y, %H:%M:%S %p')
        n = datetime_object.strftime("%d/%m/%y, %I:%M:%S %p")
        datetime_n.append(n)
    df['message_date'] = pd.to_datetime(datetime_n, format='%d/%m/%y, %I:%M:%S %p')

    for i in df['user_message']:
        entry = re.split(r":", i.strip(), maxsplit=1)
        if entry[1:]:
            user.append(entry[0].replace(":", ''))
            message.append(entry[1])
        else:
            user.append("Group notification")
            message.append(entry[1])
    df['user'] = user
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)
    df['user']=df['user'].replace('Ata konach Lagna? ❤️🙌🏻','Group notification')
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month
    df['month_name'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    period =[]
    for i, j in zip(df['message_date'].dt.hour, df['message_date'].dt.strftime('%p')):
        if i == 12 and j == 'AM':
            period.append(f"{i}{j}-{1}PM")
        elif i == 12 and j == 'PM':
            period.append(f"{i}{j}-{1}AM")
        else:
            period.append(f"{i}{j}-{i + 1}{j}")
    df['period'] =period

    user_cat = []
    for i in df['user']:
        user_cat.append(i.strip())
    df['user'] = user_cat

    df['user'] = df['user'].astype('category')

    return df
# f = open('_chat.txt','r',encoding = 'utf-8')
# data = f.read()
# df = preprocess(data)



