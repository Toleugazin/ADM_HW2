#!/usr/bin/env python
# coding: utf-8





import pandas as pd
import matplotlib as mlp
import operator
import matplotlib.pyplot as plt
#RQ_1

def funnel(df): 
    #user_ids interested in these events
    view=df[df.event_type=='view'].groupby([df.user_id]).count().index.tolist()
    cart=df[df.event_type=='cart'].groupby([df.user_id]).count().index.tolist()
    purchase=df[df.event_type=='purchase'].groupby([df.user_id]).count().index.tolist()
    complete_funnels=len((set(cart)).intersection(set(purchase)).intersection(set(view)))
    tot_ids=len(df.groupby(df.user_id).count().index)
    print({round(complete_funnels/tot_ids*100,2)})
#RQ_1 - 1
def event_types(df):

    view_mean=df[(df.event_type == "view")].groupby(['user_session']).event_type.count().mean()
    cart_mean=df[df.event_type == "cart"].groupby(['user_session']).event_type.count().mean()
    purchase_mean=df[df.event_type == "purchase"].groupby(['user_session']).event_type.count().mean()
    events={'view':view_mean,'cart':cart_mean,'purchase':purchase_mean}
    bars=pd.DataFrame(events,index=['event_type'])
    bars.plot(kind='bar',figsize=(3,5),rot=0,colormap='tab20c');
    print('Operation that users repeat more on average within a session: ',bars.idxmax(axis=1)[0])


    #RQ_1 - 2
def views_cart(df):

    cart_df=df[df.event_type=='cart'].groupby([df.user_id,df.product_id]).count()
    view_df=df[df.event_type=='view'].groupby([df.user_id,df.product_id]).count()
    view_df=cart_df.merge(view_df,how='inner',left_index=True,right_index=True,suffixes=('_cart','_view'))
    mean_views=view_df['event_time_view'].mean()

    print (round(mean_views,2))
 #RQ_1 - 2
def cart_purchase_rate(df):

    cart=df[df.event_type=='cart'].groupby([df.user_id,df.product_id]).event_type.count().mean()
    purchase=df[df.event_type=='purchase'].groupby([df.user_id, df.product_id]).event_type.count().mean()
    print (round(purchase/cart,2)*100)

 #RQ_1 - 5
def take_first(x):
    return x[0]  
    
def interval_from_firstview(df):
    df_cart=df[df.event_type=='cart'].groupby([df.product_id,df.user_id]).event_time.unique().to_frame()
    df_view=df[df.event_type=='view'].groupby([df.product_id,df.user_id]).event_time.unique().to_frame() 
    df_view = df_view.merge(df_cart,how='inner',left_index=True,right_index=True,suffixes=('_view','_cart'))
    df_cart=0
    df_view = df_view.applymap(take_first)
    df_view['event_time_view']=pd.to_datetime(df_view.event_time_view)
    df_view['event_time_cart']=pd.to_datetime(df_view.event_time_cart)
    df_view['interval'] = df_view['event_time_cart'] - df_view['event_time_view']
    mean_time = df_view['interval'].mean()
    print({mean_time})

#RQ_2 

def products_trending(df):
    sort_cat=df[df.event_type=='purchase'].groupby('category_code').category_code.count().sort_values(ascending=False).head(10)
    sort_cat.plot(figsize=(20,4),kind='bar',title='Product categories',fontsize=15,colormap='tab20c')

def top10(df):
    cat_list=df[df.event_type=='purchase'].groupby('category_code').event_type.count().sort_values(ascending=False).head(10).index.tolist()
   
    for category in cat_list:
        p_id=df[(df.event_type=='purchase') & (df.category_code==category)].groupby(df.product_id).event_type.count().sort_values(ascending=False).head(10).index.tolist()
        print (f'\nCategory: {category}')
        print (*p_id)

#RQ_3  
def avg_prod(category,df):
    #what's the brand whose prices are higher on average?
    avg_price = df[(df.event_type == 'purchase') & (df.category_code == category)].groupby(['brand']).price.mean().sort_values(ascending=False)
    print('Brands in ascending order in category:',avg_price)
    # plot indicating the average price of the products sold by the brand
    avg_price.plot(kind = "bar",figsize=(17, 14), color="blue",title="Average price of the products sold by the brand");
    plt.title("Average price of the products sold by the brand", fontsize = 18);
    plt.xlabel("Brands", fontsize = 18);
    plt.ylabel("Average Price", fontsize = 18);
    for category in df.category_code.unique():
        max_avg_price = df[df.category_code == category].groupby(['brand']).price.mean().idxmax()
        print('The brand with the highest average price in',category,'is:', max_avg_price)


#RQ_5  
 
def avg(df):
    sort_visited = df[df.event_type == 'view'].groupby([df.event_time.dt.hour]).event_type.count().sort_values(ascending = False).index
    print('Most visits', sort_visited[0])

    x = ['Monday', 'Tuesday' ,'Wednesday', 'Thursday', 'Friday', 'Saturday' , 'Sunday']
    views = df[df.event_type == 'view']
    hour_avg = []
    for i in range (0,7):
        data_Oct_M = views[views.event_time.dt.dayofweek == i]
        hourly_average = (data_Oct_M.event_type.count())/24
        hour_avg.append(hourly_average)

    plt.plot(x, hour_avg, linewidth = 1.0, color='blue');
    plt.show();

#RQ_6

def conversion_rate(df):    

    purchase_rate = df[df.event_type=='purchase'].shape[0]
    views = df[df.event_type=='view'].shape[0]
    conversion_rate = (purchase_rate / views) * 100
    print('The overall conversion rate is:',round(conversion_rate,3), '%')

def prc(df):
    purchased_category_df = df.iloc[:,[1,3]][df.iloc[:,[1,3]].event_type == 'purchase'].groupby(df['category_code']).count().iloc[:,1].to_dict()
    viewed_category_df = df.iloc[:,[1,3]][df.iloc[:,[1,3]].event_type == 'view'].groupby(df['category_code']).count().iloc[:,1].to_dict()
    conversion_category_rate = {i: round(purchased_category_df[i]/viewed_category_df[i] * 100,3) for i in purchased_category_df.keys() & viewed_category_df}
    conversion_category_rate = sorted(conversion_category_rate.items(), key=operator.itemgetter(1),reverse=True)
    print ('conversion rate in decreasing order: \n ')
    print(*conversion_category_rate[:10],sep='\n')


    purchase_rate = df[df.event_type=='purchase'].shape[0]
    plot = {k: round((v / purchase_rate)*100,2) for k, v in purchased_category_df.items()}
    plot = {key: value for key, value in plot.items() if value >= 0.2}

    labels = plot.items()
    sizes = plot.values()
    plot = list(plot)
    fig = plt.gcf()
    fig.set_size_inches(15, 10)
    plt.barh(plot, sizes, align='center', alpha=0.7, color = 'blue')
    plt.yticks(plot, labels)
    plt.ylabel('Categories')
    plt.title('Purchase rate of each category')
    plt.show()

#RQ_7


def pareto(df):

    sales_df = df[df.event_type == "purchase"].groupby([df.user_id]).price.sum().sort_values(ascending=False)

    list_sales = sales_df.tolist()
    tot_sum = sum(list_sales)
    cumulative_sum = [0]
    percentage = [0]
    i = 0
    for i in range(len(list_sales)):
        value = list_sales[i]
        cumulative_sum.append(cumulative_sum[-1] + value)
        percentage.append((cumulative_sum[-1] + value) / tot_sum)

    plt.figure(figsize=(8, 8));
    plt.title('5 Best costumers (user_id)', fontsize=15);
    sales_df.head(5).plot.pie(autopct='%.2f%%', colormap='Dark2');
    sales_df = df[df.event_type == "purchase"].groupby([df.brand]).price.sum().sort_values(ascending=False)
    list_sales = sales_df.tolist()
    tot_sum = sum(list_sales)  #Made the total sum
    cumulative_sum = [0]
    percentage = [0]
    i = 0
    for i in range(len(list_sales)):
        value = list_sales[i]
        cumulative_sum.append(cumulative_sum[-1] + value)
        percentage.append((cumulative_sum[-1] + value) / tot_sum)

    plt.figure(figsize=(8, 8));
    plt.title('5 Best sellers brands', fontsize=15);
    sales_df.head(5).plot.pie(autopct='%.2f%%');
    sales_df = df[df.event_type == "purchase"].groupby([df.category_code]).price.sum().sort_values(ascending=False)
    list_sales = sales_df.tolist()
    tot_sum = sum(list_sales)
    cumulative_sum = [0]
    percentage = [0]
    i = 0
    for i in range(len(list_sales)):
        value = list_sales[i]
        cumulative_sum.append(cumulative_sum[-1] + value)
        percentage.append((cumulative_sum[-1] + value) / tot_sum)

    plt.figure(figsize=(8, 8));
    plt.title('5 Best sellers categories', fontsize=15);
    sales_df.head(5).plot.pie(autopct='%.2f%%');
    
   



