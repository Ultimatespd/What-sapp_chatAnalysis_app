import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("what's app")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)
    # st.dataframe(df)
    user_list = df['user'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("List of the User",user_list)

    if st.sidebar.button("Show Analysis"):
        st.header("Top Statistics")
        num_message,num_words,Image_o,Video_o,num_url = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.header("Total Message")
            st.title(num_message)
        with col2 :
            st.header("Total Words")
            st.title(num_words)
        with col3 :
            st.header("Total Images Shared")
            st.title(Image_o)
        with col4 :
            st.header("Total Video Shared")
            st.title(Video_o)
        with col5 :
            st.header("Total URL Shared")
            st.title(num_url)
        # timeline Analysis
        st.title(" Monthly Message Frequency ")
        time_df,daily_time = helper.timeline_cal(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(time_df['time'],time_df['message'],color='orange')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title(" Daily Message Frequency ")
        fig, ax = plt.subplots()
        ax.plot(daily_time['only_date'], daily_time['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        col_TM1,col_TM2 = st.columns(2)
        day_timefrq, month_timefrq = helper.most_busy_DM(selected_user,df)

        with col_TM1:
            st.title("Active Day")
            fig, ax = plt.subplots()
            ax.barh(day_timefrq['day_name'], day_timefrq['message'],color='yellow')
            st.pyplot(fig)

        with col_TM2:
            st.title("Active Month")
            fig, ax = plt.subplots()
            ax.barh(month_timefrq['month_name'], month_timefrq['message'],color='yellow')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        activity_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax= sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title("Most Active User")
            top_user,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col_x,col_y = st.columns(2)
            with col_x:
                ax.bar(top_user.index,top_user.values,color='red')
                plt.xticks(rotation ='vertical')
                st.pyplot(fig)
            with col_y:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc = helper.create_worldcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words")
        MCW = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(MCW[0],MCW[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji data
        st.title("Most common used Emojis")
        new_da = helper.emoji_data(selected_user,df)
        co1,co2 = st.columns(2)
        with co1:
            st.dataframe(new_da)
        with co2:
            fig, ax = plt.subplots()
            ax.barh(new_da[0].head(10),new_da[1].head(10))
            # plt.xticks(rotation='vertical')
            st.pyplot(fig)





