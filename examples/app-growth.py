from functions import return_ga_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

ga_view_id = '100555616'
query_start_date = '2015-01-01'
query_end_date = '2017-10-15'

df_new_users = return_ga_data(
  start_date=query_start_date,
  end_date=query_end_date,
  view_id=ga_view_id,
  metrics=[
    {'expression': 'ga:goal1Completions'},
  ],
  dimensions=[
    {'name': 'ga:isoYear'},
    {'name': 'ga:isoWeek'},
  ],
  split_dates=False,
  dimensionFilterClauses=[
      {
          'operator': 'OR',
          'filters': [
              {
                  'dimensionName': 'ga:userType',
                  'not': False,
                  'expressions':[
                    'new visitor'
                  ],
                  'caseSensitive': False
              }
          ],

      }
  ],
)

df_returning_users = return_ga_data(
  start_date=query_start_date,
  end_date=query_end_date,
  view_id=ga_view_id,
  metrics=[
    {'expression': 'ga:users'},
  ],
  dimensions=[
    {'name': 'ga:isoYear'},
    {'name': 'ga:isoWeek'},
    {'name': 'ga:segment'}
  ],
  split_dates=False,
  segments=[{
      "dynamicSegment":
      {
        "name": "Sessions with app use",
        "sessionSegment":
        {
          "segmentFilters":[
          {
            "simpleSegment":
            {
              "orFiltersForSegment":
              {
                "segmentFilterClauses": [
                {
                  "metricFilter":
                  {
                    "metricName":"ga:goal1Completions",
                    "operator":"GREATER_THAN",
                    "comparisonValue":"0"
                  }
                }]
              }
            }
          }]
        }
      }
    }]
)

df_app_growth = pd.merge(df_returning_users, df_new_users, on=['ga:isoYear','ga:isoWeek'], how='outer')
df_app_growth['Week of Year'] = df_app_growth["ga:isoYear"].map(str) + df_app_growth["ga:isoWeek"].map(str)
df_app_growth.rename(columns={'ga:users': 'Weekly Active Users', 'ga:goal1Completions': 'New App Users'}, inplace=True)
df_app_growth = df_app_growth.fillna(0)
df_app_growth['New App Users (cumulative)'] = df_app_growth['New App Users'].cumsum()
# df_app_growth = df_app_growth.set_index('Week of Year')
print(df_app_growth)


def plot_dual_axis_line_chart(title, df, main_color, sub_color, grid_color, yaxis_color, xaxis_column_name, left_yaxis_column_name,
                              right_yaxis_column_name, number_of_yaxis_ticks, xaxis_tick_interval, xaxis_label_rotation_degrees,
                              yaxis_tick_width, round_yvalues_to):
    df_plot = df
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.grid(color=grid_color, linestyle='solid', linewidth=1, axis='y')

    ax1.spines['left'].set_color(yaxis_color)
    ax2.spines['left'].set_color(yaxis_color)
    ax1.spines['right'].set_color(yaxis_color)
    ax2.spines['right'].set_color(yaxis_color)
    ax1.spines['top'].set_color(yaxis_color)
    ax2.spines['top'].set_color(yaxis_color)

    ax1.plot(df_plot.index.values, df_plot[left_yaxis_column_name], main_color)
    ax1.set_xlabel(xaxis_column_name)
    ax1.set_ylabel(left_yaxis_column_name, color=main_color)
    ax1.tick_params('y', colors=main_color, width =yaxis_tick_width, length=0)

    ax2.plot(df_plot.index.values, df_plot[right_yaxis_column_name], sub_color)
    ax2.set_xlabel(xaxis_column_name)
    ax2.set_ylabel(right_yaxis_column_name, color=sub_color)
    ax2.tick_params('y', colors=sub_color, width=yaxis_tick_width, length=0)

    yaxis_left_rounded_max = int(round_yvalues_to * round(float(df_plot[left_yaxis_column_name].max()) / round_yvalues_to))
    yaxis_right_rounded_max = int(round_yvalues_to * round(float(df_plot[right_yaxis_column_name].max()) / round_yvalues_to))

    ax1.set_yticks(np.arange(0, yaxis_left_rounded_max*1.01, yaxis_left_rounded_max/number_of_yaxis_ticks))
    ax2.set_yticks(np.arange(0, yaxis_right_rounded_max*1.01, yaxis_right_rounded_max/number_of_yaxis_ticks))

    ax1.set_ylim(ymin=0, ymax=yaxis_left_rounded_max*1.02)
    ax2.set_ylim(ymin=0, ymax=yaxis_right_rounded_max*1.02)

    xticklocs = np.arange(0, len(df_plot.index.values), xaxis_tick_interval)
    ticks = df_plot[xaxis_column_name][0::xaxis_tick_interval]
    ax1.set_xticklabels(ticks)
    ax1.xaxis.set_major_locator(mticker.FixedLocator(xticklocs))
    plt.xlim([0,len(df_plot.index.values)])
    for tick in ax1.get_xticklabels():
        tick.set_rotation(xaxis_label_rotation_degrees)

    plt.title(title, y=1.08)
    fig.tight_layout()
    plt.show()

# double axis
# https://matplotlib.org/examples/api/two_scales.html

plot_dual_axis_line_chart(
    title = 'Fuuut App Growth',
    df = df_app_growth,
    main_color = '#2d6891',
    sub_color = '#d9734e',
    grid_color = '#dddddd',
    yaxis_color = '#ffffff',
    xaxis_column_name = 'Week of Year',
    left_yaxis_column_name = 'Weekly Active Users',
    right_yaxis_column_name = 'New App Users (cumulative)',
    round_yvalues_to=50,
    number_of_yaxis_ticks=5,
    xaxis_tick_interval=5,
    xaxis_label_rotation_degrees = 90,
    yaxis_tick_width=0,
)
