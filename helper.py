from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
from cleantext import clean
import seaborn as sns

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # 1. number of Messages
    num_msg = df.shape[0]
    #2. Number of words
    num_words =[]
    for i in df['message']:
        num_words.extend(i.split())
    #3. Number of Images Shared
    Image_o = df[df['message'].str.contains('image omitted')].shape[0]
    #4. Number of Video Shared
    Video_o = df[df['message'].str.contains('video omitted')].shape[0]

    extractor = URLExtract()
    url = []
    for i in df['message']:
        url.extend(extractor.find_urls(i))
    return num_msg,len(num_words),Image_o,Video_o,len(url)

def most_busy_users(df):
    x= df['user'].value_counts().head()
    df_new = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'user':'Percentage','Index':'Name'})
    return x,df_new

def create_worldcloud(selected_user,df):
    HE = open('venv/stop_hinglish.txt', 'r')
    d1 = HE.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #removing the media omitted message
    temp = df[df['user'] != 'Group notification']
    temp_omitted = temp['message'].str.contains('omitted')
    temp = temp[~temp_omitted]

    def remove_StopW(message):
        y=[]
        for word in message.lower().split():
            if word not in d1:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width =500,height=500,min_font_size=8,background_color='white')
    temp['message'] = temp['message'].apply(remove_StopW)
    emoji_FT = []
    for i in temp['message']:
        # print()
        emoji_FT.append(clean(i, no_emoji=True))
    temp['message'] = emoji_FT
    df_wc = wc.generate(temp['message'].str.cat(sep =" "))
    return df_wc

def most_common_words(selected_user,df):
    HE = open('venv/stop_hinglish.txt', 'r')
    d1 = HE.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #removing the media omitted message
    temp = df[df['user'] != 'Group notification']
    temp_omitted = temp['message'].str.contains('omitted')
    temp = temp[~temp_omitted]
    emoji_FT = []
    for i in temp['message']:
        # print()
        emoji_FT.append(clean(i, no_emoji=True))
    temp['message'] = emoji_FT
    #removing the hin-eng stopwords
    word_sw = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in d1:
                word_sw.append(word.strip())
    data_CW = pd.DataFrame(Counter(word_sw).most_common(20))
    return data_CW

def emoji_data(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis=[]
    for e in df['message']:
        # em.extend([i for i in e if i in emoji.EMOJI_DATA])
        emojis.extend(emoji.distinct_emoji_list(e))
    em_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return em_df

def timeline_cal(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_name', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month_name'][i]}-{timeline['year'][i]}")
    timeline['time'] = time
    df['only_date'] = df['message_date'].dt.date
    daily_time = df.groupby(['only_date']).count()['message'].reset_index()

    return timeline,daily_time

def most_busy_DM(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    day_timefrq = df.groupby(['day_name']).count()['message'].reset_index()
    month_timefrq = df.groupby(['month_name']).count()['message'].reset_index()
    return day_timefrq,month_timefrq

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_activity_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_activity_heatmap