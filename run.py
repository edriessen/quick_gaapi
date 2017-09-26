from functions import return_ga_data, save_df_to_excel

df = return_ga_data(
  start_date='2017-09-13',
  end_date='2017-09-21',
  view_id='100555616',
  metrics=[{'expression': 'ga:sessions'},],
  dimensions=[{'name': 'ga:source'}],
  split_dates=False,
  group_by=[]
)

print(df)

# save_df_to_excel(
#   df=df,
#   path='C:\\Users\\Erik\\Documents\\',
#   file_name='test_export',
#   sheet_name='data'
# )
