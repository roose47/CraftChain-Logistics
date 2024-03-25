import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from joblib import load
import datetime
from sklearn.ensemble import RandomForestRegressor

model = load('./fabapp/svr_model.joblib')
# Create your views here.
store_sales = pd.read_csv("./fabapp/Datasets/all_orders.csv")

supervised_data = pd.read_csv("./fabapp/Datasets/supervised_data.csv")

today_datetime = datetime.datetime.now()

# Format the datetime object to the desired format

# print("store_sales", store_sales)


        # future_dates = pd.date_range(start=pd.Timestamp('2023-03-01 00:00:00') + pd.DateOffset(months=1), periods=12, freq='MS')print(store_sales)
store_sales.rename(columns={'Sales Date': 'date', 'Price': 'sales'}, inplace=True)
store_sales['date'] =  pd.to_datetime(store_sales['date'])
store_sales['date'] = store_sales['date'].dt.to_period("M")

top_product_sales = pd.read_csv("./fabapp/Datasets/top_products.csv")



model_for_junctionboxS = load('./fabapp/ml_models/JunctionBox(S)_svr_model.pkl')
model_for_msbrackets = load('./fabapp/ml_models/MSBrackets_svr_model.pkl')
model_for_msplatform = load('./fabapp/ml_models/MSPLatform_svr_model.pkl')
model_for_sheetmetalboxes = load('./fabapp/ml_models/SheetMetalBoxes_svr_model.pkl')
model_for_squaresheetjb = load('./fabapp/ml_models/SquareSheetMetalJunctionBox_svr_model.pkl')

di = {
    'MS Brackets': model_for_msbrackets, 
    'Square Sheet Metal Junction Box': model_for_squaresheetjb, 
    'Sheet Metal Boxes':model_for_sheetmetalboxes, 
    'Junction Box (S)':model_for_junctionboxS, 
    'MS PLatform':model_for_msplatform
    }


def get_prediction():
    formatted_datetime = today_datetime.strftime('%Y-%m-%d')
    # print("sffasdfaf" ,formatted_datetime)
    future_dates = pd.date_range(start=pd.Timestamp(formatted_datetime) + pd.DateOffset(months=1), periods=12, freq='MS')

    future_dates = pd.DataFrame(future_dates, columns=['date'])

    #optional
    monthly_sales = store_sales.groupby('date').sum().reset_index() #reset_index to keep the index
    # print("monthly_sales", monthly_sales)
    # monthly_sales

    monthly_sales['month'] = monthly_sales['date'].dt.month

    monthly_sales = monthly_sales.groupby('month')['sales'].mean().reset_index()

    monthly_sales['sales_diff'] = monthly_sales['sales'].diff()
    monthly_sales = monthly_sales.dropna()
    

    future_sales_diff = []
    for i in range(1, 12): #was 13
        col_name = 'month_' + str(i)
        # print(monthly_sales['sales_diff'].iloc[-i])
        future_sales_diff.append(monthly_sales['sales_diff'].iloc[-i])

    # Convert to array and reshape for compatibility with scaler
    future_sales_diff = np.array(future_sales_diff)
    # print("future_sales_difference ",future_sales_diff)

    future_sales_diff = pd.DataFrame(future_sales_diff, columns=['sales_diff'])

    for i in range(1, 13):
        col_name = 'month_' + str(i)
        future_sales_diff[col_name] = future_sales_diff['sales_diff'].shift(i)

        # Fill NaN values with 0
    future_sales_diff.fillna(0, inplace=True)

        # Drop rows with NaN values
    future_sales_diff = future_sales_diff.dropna().reset_index(drop=True)
    scaler = MinMaxScaler(feature_range=(-1,1))
    train_data = supervised_data[:-35]
    scaler.fit(train_data)
    final_test_data = scaler.transform(future_sales_diff)

    X_test, y_test = final_test_data[:,1:], final_test_data[:, 0:1]

    # y_test = y_train.ravel()

    future_dates = future_dates['date'].reset_index(drop=True)

    final_predict_df = pd.DataFrame(future_dates)

    svr_pre =  model.predict(X_test)

    svr_pre = svr_pre.reshape(-1,1)

    svr_pre_test_set = np.concatenate([svr_pre, X_test], axis = 1)

    svr_pre_test_set = scaler.inverse_transform(svr_pre_test_set) #get actual values back

    # result_list = []   #why this step????
    # for index in range(0, len(svr_pre_test_set)):
    #     result_list.append(svr_pre_test_set[index][0])

    actual_sales = monthly_sales['sales'][-12:].to_list()

    result_list = []   #why this step????
    for index in range(0, len(svr_pre_test_set)):
        # print(svr_pre_test_set[index][0], actual_sales[index])
        result_list.append(svr_pre_test_set[index][0] + actual_sales[index])

    result_list = np.round(result_list).astype(int)
    svr_pre_series = pd.Series(result_list, name="SVM Prediction")
    final_predict_df['date'] = final_predict_df['date'].astype(str)
    # print(final_predict_df['date'].dtype)
    final_predict_df = final_predict_df.merge(svr_pre_series, left_index=True, right_index = True)
    # print(final_predict_df)
    return final_predict_df
    # print(final_predict_df)

def get_demand():
    prediction_dfs = []
    for product in ['MS Brackets', 'Square Sheet Metal Junction Box', 'Sheet Metal Boxes', 'Junction Box (S)', 'MS PLatform']:#,'Square Sheet Metal Junction Box', 'Sheet Metal Boxes', 'Junction Box (S)', 'MS PLatform'
        
        # print(f"*******************{product}********************")
        future_dates = pd.date_range(start=pd.Timestamp('2023-03-01 00:00:00') + pd.DateOffset(months=1), periods=12, freq='MS')
        future_dates = pd.DataFrame(future_dates, columns=['date'])
        # print("top_product_sales", top_product_sales)
        top_product_sales.rename(columns={'Sales Date': 'date', 'Quantity': 'sales'}, inplace=True)
        top_product_sales['date'] =  pd.to_datetime(top_product_sales['date'])
        product_data = top_product_sales[top_product_sales['Product Name'] == product]
        
        product_data = product_data.drop(['Product Name', 'Price'], axis=1)

        monthly_sales = product_data.groupby('date').sum().reset_index()
        monthly_sales = monthly_sales.iloc[2:]
        # print(monthly_sales)
        # monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()# Convert date to datetime
        monthly_sales['sales_diff'] = monthly_sales['sales'].diff()
        monthly_sales = monthly_sales.dropna()
        

        supervised_data = monthly_sales.drop(['date', 'sales'], axis=1)
        
        for i in range(1, 13):
            col_name = 'month_' + str(i)
            supervised_data[col_name] = supervised_data['sales_diff'].shift(i)
        # Fill NaN values with 0
        supervised_data.fillna(0, inplace=True)
        # print(supervised_data)
        # Drop rows with NaN values
        supervised_data = supervised_data.dropna().reset_index(drop=True)
        # print(monthly_sales)
        train_data = supervised_data[:-36]
        scaler = MinMaxScaler(feature_range=(0,1))
        scaler.fit(train_data)
        
        
        future_sales_diff = []
        for i in range(1, 12): #was 13
            col_name = 'month_' + str(i)
            # print(monthly_sales['sales_diff'].iloc[-i])
            future_sales_diff.append(monthly_sales['sales_diff'].iloc[-i])

        future_sales_diff = np.array(future_sales_diff)

        future_sales_diff = pd.DataFrame(future_sales_diff, columns=['sales_diff'])

        for i in range(1, 13):
            col_name = 'month_' + str(i)
            future_sales_diff[col_name] = future_sales_diff['sales_diff'].shift(i)
        
        future_sales_diff.fillna(0, inplace=True)
        # Drop rows with NaN values
        future_sales_diff = future_sales_diff.dropna().reset_index(drop=True)
       
        final_test_data = scaler.transform(future_sales_diff)

        X_test, y_test = final_test_data[:,1:], final_test_data[:, 0:1]

        # print(future_dates)
        future_dates = future_dates['date'].reset_index(drop=True)

        final_predict_df = pd.DataFrame(future_dates)

        for name, model in di.items():
            if product == name:
            # model.fit(X_train, y_train)
                svr_pre =  model.predict(X_test)
                # print('len of svm_pre', len(svr_pre))
                svr_pre = svr_pre.reshape(-1,1)
                svr_pre_test_set = np.concatenate([svr_pre, X_test], axis = 1)
                svr_pre_test_set = scaler.inverse_transform(svr_pre_test_set) #get actual values back


                actual_sales = monthly_sales['sales'][-12:].to_list()

                result_list = []   #why this step????
                for index in range(0, len(svr_pre_test_set)):
                    # print(svr_pre_test_set[index][0], actual_sales[index])
                    result_list.append(svr_pre_test_set[index][0] + actual_sales[index])
                result_list = np.round(result_list).astype(int)
                svr_pre_series = pd.Series(result_list, name="SVM Prediction")
                final_predict_df['date'] = final_predict_df['date'].astype(str)
                final_predict_df = final_predict_df.merge(svr_pre_series, left_index=True, right_index = True)
                prediction_dfs.append(final_predict_df)
                # print("XDDDDDDDDDDDDDD")
                # print(prediction_dfs)
    return prediction_dfs
# models = {'Random Forest': RandomForestRegressor()}
# store_sales = pd.read_csv("./fabapp/Datasets/top_products.csv")
# store_sales.rename(columns={'Sales Date': 'date', 'Quantity': 'sales'}, inplace=True)
# store_sales = store_sales.drop(['Price'], axis=1)
# store_sales['date'] =  pd.to_datetime(store_sales['date'])

# def get_demand():
#     for product in ['MS Brackets', 'Square Sheet Metal Junction Box', 'Sheet Metal Boxes', 'Junction Box (S)', 'MS PLatform']:
#         print(f"*******************{product}********************")
        
#         # print(store_sales)
#         # store_sales = df
#         # print(store_sales)
#         product_data = store_sales[store_sales['Product Name'] == product]
#         # print(product_data)
#         # store_sales['date'] = store_sales['date'].dt.to_period("M") #remove the day in the date
#         monthly_sales = product_data.groupby('date').sum().reset_index() #reset_index to keep the index
#         # print("Monthly Sales", len(monthly_sales))
#         # print(monthly_sales)
#         # monthly_sales['date'] = monthly_sales['date'].dt.to_timestamp()
#         monthly_sales['sales_diff'] = monthly_sales['sales'].diff()
#         monthly_sales = monthly_sales.dropna()
#         print("fsfsdgsgsgsgsgsg")
#         supervised_data = monthly_sales.drop(['date', 'sales'], axis=1)
#         for i in range(1, 13):
#             col_name = 'month_' + str(i)
#             supervised_data[col_name] = supervised_data['sales_diff'].shift(i)

#         # Fill NaN values with 0
#         supervised_data.fillna(0, inplace=True)

#         # Drop rows with NaN values
#         supervised_data = supervised_data.dropna().reset_index(drop=True)
#         # print(supervised_data)
#         train_data = supervised_data.drop(['Product Name'], axis=1)[:-24]  # Modify this line
#         test_data = supervised_data.drop(['Product Name'], axis=1)[-48:]  # Modify this line
#         # print(train_data)
#         scaler = MinMaxScaler(feature_range=(-1,1))
#         scaler.fit(train_data)
#         train_data = scaler.transform(train_data) #scaling values to a specific range
#         # print(scaler)
#         test_data = scaler.transform(test_data)
#         X_train , y_train = train_data[:, 1:], train_data[:,0:1]
#         X_test, y_test = test_data[:,1:], test_data[:, 0:1]
#         y_test = y_train.ravel()
#         y_train = y_train.ravel()
#         sales_dates = monthly_sales['date'][-48:].reset_index(drop=True) #get last 12 months dates
#         predict_df = pd.DataFrame(sales_dates) #put the dates in a dataframe to act as input
#         actual_sales = monthly_sales['sales'][-48:].to_list()  #get last 12 month sales
#         for name, model in models.items():
#             model.fit(X_train, y_train)
#             svr_pre = model.predict(X_test)
#             svr_pre = svr_pre.reshape(-1, 1)
#             svr_pre_test_set = np.concatenate([svr_pre, X_test], axis=1)
#             svr_pre_test_set = scaler.inverse_transform(svr_pre_test_set)
#             result_list = []
#             for index in range(0, len(svr_pre_test_set)):
#                 result_list.append(svr_pre_test_set[index][0] + actual_sales[index])
#             svr_pre_series = pd.Series(result_list, name="SVM Prediction")
#             predict_df = predict_df.merge(svr_pre_series, left_index=True, right_index=True, suffixes=('', '_'+name))
#             print(predict_df)
#     return predict_df

# def get_demand():
#     today_datetime = datetime.datetime.now()
#     formatted_datetime = today_datetime.strftime('%Y-%m-%d')
#     print("sffasdfaf" ,formatted_datetime)
#     future_dates = pd.date_range(start=pd.Timestamp(formatted_datetime) + pd.DateOffset(months=1), periods=12, freq='MS')
#     store_sales.rename(columns={'Sales Date': 'date', 'Price': 'sales'}, inplace=True)
#     store_sales['date'] =  pd.to_datetime(store_sales['date'])
#     future_dates = pd.DataFrame(future_dates, columns=['date'])
#     monthly_sales = store_sales.groupby('date').sum().reset_index()
#     monthly_sales['month'] = monthly_sales['date'].dt.month
#     monthly_sales = monthly_sales.groupby('month')['sales'].mean().reset_index()
#     monthly_sales['sales_diff'] = monthly_sales['sales'].diff()
#     monthly_sales = monthly_sales.dropna()
#     future_sales_diff = []
#     for i in range(1, 12):
#         col_name = 'month_' + str(i)
#         print(monthly_sales['sales_diff'].iloc[-i])
#         future_sales_diff.append(monthly_sales['sales_diff'].iloc[-i])

#     # Convert to array and reshape for compatibility with scaler
#     future_sales_diff = np.array(future_sales_diff)
#     future_sales_diff = pd.DataFrame(future_sales_diff, columns=['sales_diff'])
#     for i in range(1, 13):
#         col_name = 'month_' + str(i)
#         future_sales_diff[col_name] = future_sales_diff['sales_diff'].shift(i)

#     # Fill NaN values with 0
#     future_sales_diff.fillna(0, inplace=True)

#     # Drop rows with NaN values
#     future_sales_diff = future_sales_diff.dropna().reset_index(drop=True)

#     for i in range(1, 13):
#         col_name = 'month_' + str(i)
#         supervised_data[col_name] = supervised_data['sales_diff'].shift(i)

#     # Fill NaN values with 0
#     supervised_data.fillna(0, inplace=True)

#     # Drop rows with NaN values
#     supervised_data = supervised_data.dropna().reset_index(drop=True)

#     train_data = supervised_data[:-24]

#     scaler = MinMaxScaler(feature_range=(-1,1))
#     scaler.fit(train_data)

#     final_test_data = scaler.transform(future_sales_diff)