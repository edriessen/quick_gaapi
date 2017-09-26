import pandas as pd
import config
from datetime import datetime, timedelta
from time import sleep

def convert_reponse_to_df(response):
  list = []
  # parse report data
  for report in response.get('reports', []):

    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])

    for row in rows:
        dict = {}
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
          dict[header] = dimension

        for i, values in enumerate(dateRangeValues):
          for metric, value in zip(metricHeaders, values.get('values')):
            if ',' in value or ',' in value:
              dict[metric.get('name')] = float(value)
            else:
              dict[metric.get('name')] = int(value)
        list.append(dict)

    df = pd.DataFrame(list)
    return df


def get_report(analytics, start_date, end_date, view_id, metrics, dimensions):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': view_id,
          'dateRanges': [{'startDate':start_date, 'endDate': end_date}],
          'metrics': metrics,
          'dimensions': dimensions,
        }]
      }
  ).execute()


def return_ga_data(start_date, end_date, view_id, metrics, dimensions, split_dates, group_by=False):
    if split_dates == False:
        return convert_reponse_to_df(get_report(config.service, start_date, end_date, view_id, metrics, dimensions))
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        delta = end_date - start_date         # timedelta
        dates = []

        for i in range(delta.days + 1):
            dates.append(start_date + timedelta(days=i))

        df_total = pd.DataFrame()
        for date in dates:
            date = str(date)
            df_total = df_total.append(convert_reponse_to_df(get_report(config.service, date, date, view_id, metrics, dimensions)))
            sleep(1)

        if len(group_by) != 0:
            df_total = df_total.groupby(group_by).sum()

        return df_total


def save_df_to_excel(df, path, file_name, sheet_name):
    writer = pd.ExcelWriter(path+file_name+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
