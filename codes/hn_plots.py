# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:48:42 2018
"""

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def todays_date():
    
    """Returns today's date in 'YYYYMMDD' format"""
    
    todays_date = datetime.now()
    if todays_date.month <10:
        month = '0'+str(todays_date.month)
    else:
        month = str(todays_date.month)
    
    if todays_date.day <10:
        day = '0'+str(todays_date.day)
    else:
        day = str(todays_date.day)
    
    date = str(todays_date.year) + month + day
    return date

### hn_plots - function to plot 4 time series at once
###             for the needs of analysis of data from Hacker News (HN) and
###             Stack Overflow (SO)    

def hn_plots(data,
             freq = 'd',
             select_tech = ['d3js', 'javascript', 'tensorflow'],
             alpha = 0.7,
             after_date = '2017-01-01',
             output_date = todays_date(),
             common_var = 'hn_all_match_score',
             common_var2 = None,
             common_var3 = None,
             common_var4 = None,
             var1 = 'so_usage_cnt',
             var2 = 'so_score_sum',
             var3 = 'so_answers',
             var4 = 'so_views',
             subfolder = None,
             add_freq_label = True,
             same_oy = False,
             label1 = None,
             label2 = None,
             label3 = None,
             label4 = None,
             show_y_lab = True,
             col1 = 'g-',
             col2 = 'b-'):
    
    """
    PARAMETERS:
    1) data - input data
    2) freq - frequency of time series aggregation
    3) select_tech - technologies, for which data should be plotted
    4) alpha - transparency level
    5) after_date - date, from which time series should be plotted
    6) output_date - date of plot creation, goes to the name of outputted
        .png file
    7) common_var - first time series which is used for all four plots
        (if not specified otherwise)
    8) common_var2, common_var3, common_var4 - first time series
        for the second, third and fourth plot (if not specified, `common_var`
        is used)
    9) var1, var2, var3, var4 - second time series used for consecutive
        plots (each has to be specified separately)
    10) add_freq_label - boolean value indicating whether the information
        about frequency should be put in titles of plots
    11) same_oy - booleand value indicating whether two lines on a given
        plot should share the OY axis.
    12) label1, label2, label3, label4 - titles for consecutive plotsł
        if not specified, default titles are used
    13) show_y_lab - boolean value indicating whether labels for the first
        and second Y axes should be shown
    14) col1, col2 - color for the first and second line on the plot
    """
    
    if(freq == 'w'):
        data = (data.groupby(['tech',
                       pd.Grouper(key = 'date', freq = 'W-MON')])
                .sum()
                .reset_index())
        freq_label = 'weekly'
    elif(freq == 'd'):
        freq_label = 'daily'
    elif(freq == 'M'):
        data = (data.groupby(['tech',
                       pd.Grouper(key = 'date', freq = freq)])
                .sum()
                .reset_index())
        freq_label = 'monthly'
    if add_freq_label == False:
        freq_label = ''
     
    if common_var2 == None:
        common_var2 = common_var
    if common_var3 == None:
        common_var3 = common_var
    if common_var4 == None:
        common_var4 = common_var
        
    after_date_declared = after_date
    
    if subfolder == None:
        subfolder = ''
    else:
        subfolder = '.\\' + subfolder + '\\'
        
    for i in select_tech:
        
        fig_daily = plt.figure(figsize = (16,10))
        fig_daily.subplots_adjust(hspace = 0.3)
        fig_daily.tight_layout()
        ax1 = plt.subplot(221)
        ax3 = plt.subplot(222)
        ax5 = plt.subplot(223)
        ax7 = plt.subplot(224)
        if same_oy == True:
            ax2 = ax1
            ax4 = ax3
            ax6 = ax5
            ax8 = ax7
        else:
            ax2 = ax1.twinx()
            ax4 = ax3.twinx()
            ax6 = ax5.twinx()
            ax8 = ax7.twinx()
        ax1.tick_params(axis='x', labelrotation =30)
        ax2.tick_params(axis='x', labelrotation =30)
        ax3.tick_params(axis='x', labelrotation =30)
        ax4.tick_params(axis='x', labelrotation =30)
        ax5.tick_params(axis='x', labelrotation =30)
        ax6.tick_params(axis='x', labelrotation =30)
        ax7.tick_params(axis='x', labelrotation =30)
        ax8.tick_params(axis='x', labelrotation =30)
        
        # First plot:
        after_date = (max(pd.to_datetime(after_date_declared),
                        data.loc[(data['tech'] == i) &
                                 ((data['hn_all_match_score'] > 0) | 
                                         (data['so_views']>0))]
            .date.min()).strftime('%Y-%m-%d'))
  
        data_plot = data.loc[(data['tech'] == i) & (data['date'] >= after_date)]
        ax1.plot(data_plot['date'], data_plot[common_var], color = col1,
                 alpha = alpha, label = 'HN')
        ax2.plot(data_plot['date'], data_plot[var1], color = col2,
                 alpha = alpha, label = 'SO')
        
        if show_y_lab == True:
            ax1.set_ylabel('HN', color = col1)
            ax2.set_ylabel('SO', color = col2)
        if label1 == None:
            ax2.set_title(var1 + ' vs ' + common_var + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        else:
            ax2.set_title(label1)
        ax1.legend(loc = 2)
        ax2.legend(loc = 2)
        
        
        # Second plot: 
        ax3.plot(data_plot['date'], data_plot[common_var2], color = col1,
                 alpha = alpha, label = 'HN')
        ax4.plot(data_plot['date'], data_plot[var2], color = col2,
                 alpha = alpha, label = 'SO')

        if show_y_lab == True:
            ax3.set_ylabel('HN', color = col1)
            ax4.set_ylabel('SO', color = col2)
        if label2 == None:
            ax4.set_title(var2 + ' vs ' + common_var2 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        else:
            ax4.set_title(label2)
        ax4.legend(loc = 2)
    
        # Third plot: 
        ax5.plot(data_plot['date'], data_plot[common_var3], color = col1,
                 alpha = alpha, label = 'HN')
        ax6.plot(data_plot['date'], data_plot[var3], color = col2,
                 alpha = alpha, label = 'SO')

        if show_y_lab == True:
            ax5.set_ylabel('HN', color = col1)
            ax6.set_ylabel('SO', color = col2)
        if label3 == None:
            ax6.set_title(var3 + ' vs ' + common_var3 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        else:
            ax6.set_title(label3)
        ax6.legend(loc = 2)
        
        # Fourth plot: 
        ax7.plot(data_plot['date'], data_plot[common_var4], color = col1,
                 alpha = alpha, label = 'HN')
        ax8.plot(data_plot['date'], data_plot[var4], color = col2,
                 alpha = alpha, label = 'SO')

        if show_y_lab == True:
            ax7.set_ylabel('HN', color = col1)
            ax8.set_ylabel('SO', color = col2)
        if label4 == None:
            ax8.set_title(var4 + ' vs ' + common_var4 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        else:
            ax8.set_title(label4)
        ax8.legend(loc = 2)
        

        plt.xticks(rotation=90)

        fig_daily.savefig(subfolder + output_date + '_' + i + '_' + common_var +
                          '_' +
                          common_var2 + '_' + common_var3 + '_' + common_var4 +
                          '_'+ freq + '_since' + after_date.replace('_', '')
                          + '.png'
                          )
        
### End of code