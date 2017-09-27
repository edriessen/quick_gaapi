import pandas as pd
from config import service
from datetime import datetime
from dateutil.rrule import rrule, DAILY
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
          'pageSize': 10000,
        }]
      }
  ).execute()


def return_ga_data(start_date, end_date, view_id, metrics, dimensions, split_dates, group_by=False):
    if split_dates == False:
        return convert_reponse_to_df(get_report(config.service, start_date, end_date, view_id, metrics, dimensions))
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        df_total = pd.DataFrame()
        for date in rrule(freq=DAILY, dtstart=start_date, until=end_date):
            date = str(date.date())
            df_total = df_total.append(convert_reponse_to_df(get_report(service, date, date, view_id, metrics, dimensions)))
            sleep(1)

        if len(group_by) != 0:
            df_total = df_total.groupby(group_by).sum()

        return df_total


def save_df_to_excel(df, path, file_name, sheet_name):
    writer = pd.ExcelWriter(path+file_name+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    writer.save()
