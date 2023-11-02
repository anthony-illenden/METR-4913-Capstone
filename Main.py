import requests
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.patches import Patch
import matplotlib.patches as mpatches
from cartopy.mpl.geoaxes import GeoAxes
import metpy
from metpy.io import parse_metar_file
from metpy.plots import USCOUNTIES
import pandas as pd
from datetime import datetime

def Read():
    local_csv = pd.read_csv('C:\\Users\\Tony\\Desktop\\Capstone\\farpod4.csv')
    return local_csv

def Calculate(station_list,date1,month1,year1,time1,date2,time2,month2,year2,wfo):
    website_date1 = int(date1[date1.find('/')+1:date1.find('/')+3])
    website_date2 = int(date2[date2.find('/')+1:date2.find('/')+3])
    mi_url = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=ACB&station=ADG&station=AMN&station=ANJ&station=APN&station=ARB&station=AZO&station=BAX&station=BEH&station=BIV&station=BTL&station=CAD&station=CFS&station=CIU&station=CMX&station=CVX&station=D95&station=DET&station=DRM&station=DTW&station=DUH&station=ERY&station=ESC&station=FFX&station=FKS&station=FNT&station=FPK&station=GLR&station=GOV&station=GRR&station=HAI&station=HTL&station=HYX&station=IKW&station=IMT&station=IRS&station=ISQ&station=IWD&station=JXN&station=JYM&station=LAN&station=LDM&station=LWA&station=MBL&station=MBS&station=MCD&station=MGN&station=MKG&station=MNM&station=MOP&station=MTC&station=OEB&station=ONZ&station=OSC&station=OZW&station=P53&station=P58&station=P59&station=P75&station=PHN&station=PLN&station=PTK&station=PZQ&station=RMY&station=RNP&station=RQB&station=SAW&station=SJX&station=SLH&station=TEW&station=TTF&station=TVC&station=VLL&station=Y31&station=Y70&station=YIP&data=all&year1='+str(year1)+'&month1='+str(month1)+'&day1='+str(website_date1)+'&year2='+str(year2)+'&month2='+str(month2)+'&day2='+str(website_date2+1)+'&tz=Etc%2FUTC&format=onlycomma&latlon=yes&elev=no&missing=M&trace=T&direct=no&report_type=3&report_type=4'    #in_url = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?data=all&year1=2022&month1=11&day1='+str(website_date1)+'&year2=2022&month2=11&day2='+str(website_date2+1)+'&tz=Etc%2FUTC&format=onlycomma&latlon=yes&elev=no&missing=M&trace=T&direct=no&report_type=1&report_type=3&report_type=4'
    in_url = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=1II&station=2R2&station=4I7&station=AID&station=ANQ&station=ASW&station=BAK&station=BFR&station=BMG&station=C62&station=C65&station=CFJ&station=DCY&station=EKM&station=EVV&station=EYE&station=FKR&station=FRH&station=FWA&station=GEZ&station=GGP&station=GPC&station=GSH&station=GUS&station=GWB&station=GYY&station=HBE&station=HFY&station=HHG&station=HLB&station=HNB&station=HUF&station=IMS&station=IND&station=JVY&station=LAF&station=MCX&station=MGC&station=MIE&station=MQJ&station=MZZ&station=OKK&station=OXI&station=PLD&station=PPO&station=RCR&station=RID&station=RZL&station=SBN&station=TYQ&station=UMP&station=UWL&station=VPZ&data=all&year1='+str(year1)+'&month1='+str(month1)+'&day1='+str(website_date1)+'&year2='+str(year2)+'&month2='+str(month2)+'&day2='+str(website_date2+1)+'&tz=Etc%2FUTC&format=onlycomma&latlon=yes&elev=no&missing=M&trace=T&direct=no&report_type=1&report_type=3&report_type=4'
    df_parsed1 = pd.read_csv(mi_url)
    df_parsed2 = pd.read_csv(in_url)
    df_parsed = pd.concat([df_parsed1, df_parsed2], ignore_index=True)


    wx_list = df_parsed['wxcodes'].unique()
    snow_list = []

    for i in wx_list:
        if 'SN' in i:
            snow_list.append(i)

    snow_sum = 0
    total = 0
    print(datetime.strptime(date1+' '+time1,'%m/%d/%Y %H:%M'))
    for i in station_list:
        total_df = df_parsed[(df_parsed['station'] == i) & (pd.to_datetime(df_parsed['valid'],format='%Y-%m-%d %H:%M') >= datetime.strptime(date1+' '+time1,'%m/%d/%Y %H:%M')) & (pd.to_datetime(df_parsed['valid'],format='%Y-%m-%d %H:%M') <= datetime.strptime(date2+' '+time2,'%m/%d/%Y %H:%M'))]
        total += len(total_df)
        for j in snow_list:
            snow_df_parsed = total_df[(total_df['station'] == i) & (total_df['wxcodes'] == j)]
            #print(new_df_parsed)
            snow_sum += len(snow_df_parsed)
    vsbylist = []
    total_df['vsby'] = total_df['vsby'].astype('float')
    for i in range(0, len(total_df['vsby'])):
        data = total_df['vsby'].iloc[i]
        if data >= 1: 
            output = 'light'
        elif data >= .5:
            output = 'moderate'
        else:
            output = 'heavy'
        vsbylist.append(output)
            
    total_df['vsby_literal'] = vsbylist 
    no_snow = total - snow_sum

    print(snow_sum)
    print(no_snow)
    print((snow_sum/total)*100)
    print((no_snow/total)*100)

    print(len(total_df[total_df['vsby_literal'] == 'light']) / len(total_df['vsby_literal']))
    print(len(total_df[total_df['vsby_literal'] == 'moderate']) / len(total_df['vsby_literal']))
    print(len(total_df[total_df['vsby_literal'] == 'heavy']) / len(total_df['vsby_literal']))
    lgt = len(total_df[total_df['vsby_literal'] == 'light']) / len(total_df['vsby_literal'])
    mod = len(total_df[total_df['vsby_literal'] == 'moderate']) / len(total_df['vsby_literal'])
    hvy = len(total_df[total_df['vsby_literal'] == 'heavy']) / len(total_df['vsby_literal'])

    df2 = {'startdate': datetime.strptime(date1+' '+time1,'%m/%d/%Y %H:%M'),
           'enddate': datetime.strptime(date2+' '+time2,'%m/%d/%Y %H:%M'),
           'wfo': wfo,
           'far': no_snow,
           'pod': snow_sum,
           'far_pct': round((no_snow/total)*100, 3),
           'pod_pct': round((snow_sum/total)*100, 3),
           'lgt': len(total_df[total_df['vsby_literal'] == 'light']),
           'mod': len(total_df[total_df['vsby_literal'] == 'moderate']),
           'hvy': len(total_df[total_df['vsby_literal'] == 'heavy']),
           'lgt_pct': round((lgt)*100, 3),
           'mod_pct': round((mod)*100, 3),
           'hvy_pct': round((hvy)*100, 3)}
    return df2

def Write(local_csv,df2):
    local_csv.loc[-1] = df2
    local_csv.index = local_csv.index + 1  # shifting index
    local_csv = local_csv.sort_index()  # sorting by index
    local_csv.to_csv('C:\\Users\\Tony\\Desktop\\Capstone\\farpod4.csv',index=False)

def main():
    date1 = '12/18/2019'
    month1 = '12' 
    year1 = '2019'
    time1 = '16:44'
    date2 = '12/18/2019'
    month2 = '12' 
    year2 = '2019'
    time2 = '20:10'
    wfo = 'apx'
    station_list = ['CVX','BFA','GLR','ACB','TVC','GOV','FKS','CAD'] 
    local_csv = Read()
    df2 = Calculate(station_list,date1,month1,year1,time1,date2,time2,month2,year2,wfo)
    Write(local_csv,df2)

if __name__ == '__main__':
    main()
