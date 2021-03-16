import pandas as pd
import datetime, os, pkg_resources

def __load_df():
    stream = pkg_resources.resource_stream(__name__, '절입데이터.csv')
    df = pd.read_csv(stream)
    for i in range(1, 25):
        df.iloc[:,i] = df.iloc[:,0].astype(str) + '년 ' + df.iloc[:,i]
    df = df.set_index('연도')

    # parse to datetime
    for col in df.keys():
        df[col] = df[col].apply(lambda x : datetime.datetime.strptime(x, '%Y년 %m월 %d일'))
    return df

def parse(year, month, day):
    '''
    parse date into three pillars of korean fortune telling.
    currently supports year, month, and day pillars. results are only accurate if input year is between 1900 and 2050.
    NOTICE -- it is recommended to check the validity of year/month/day with the datetime module before passing arguments.
    
    year : integer (e.g. 1995)
    month : integer of 1~12 (e.g. 11)
    day : integer of 1~28/29/30/31 (e.g. 16)
    return : string (e.g. '을해, 정해, 신해')
    '''
    def __parse_year(year):
        dict_year1 = {4:'갑', 5:'을', 6:'병', 7:'정', 8:'무', 9:'기', 0:'경', 1:'신', 2:'임', 3:'계'}
        dict_year2 = {4:'자', 5:'축', 6:'인', 7:'묘', 8:'진', 9:'사', 10:'오', 11:'미', 0:'신', 1:'유', 2:'술', 3:'해'}
        index_year1 = year % 10
        index_year2 = year % 12
        result_year = ''.join([dict_year1[index_year1], dict_year2[index_year2]])
        return result_year
    
    # parse year
    result_year = __parse_year(year)
        
    # parse month
    date = datetime.datetime(year, month, day)
    try:
        srs = __lunar_months_df.loc[year]
        if date < srs.loc['소한']:
            temp_year, temp_month = year - 1, 11
        elif (srs.loc['소한'] <= date) & (date < srs.loc['경칩']):
            temp_year, temp_month = year - 1, 12
        elif (srs.loc['입춘'] <= date) & (date < srs.loc['경칩']):
            temp_year, temp_month = year, 1
        elif (srs.loc['경칩'] <= date) & (date < srs.loc['청명']):    
            temp_year, temp_month = year, 2
        elif (srs.loc['청명'] <= date) & (date < srs.loc['입하']):
            temp_year, temp_month = year, 3
        elif (srs.loc['입하'] <= date) & (date < srs.loc['망종']):    
            temp_year, temp_month = year, 4
        elif (srs.loc['망종'] <= date) & (date < srs.loc['소서']):
            temp_year, temp_month = year, 5
        elif (srs.loc['소서'] <= date) & (date < srs.loc['입추']):
            temp_year, temp_month = year, 6
        elif (srs.loc['입추'] <= date) & (date < srs.loc['백로']):
            temp_year, temp_month = year, 7
        elif (srs.loc['백로'] <= date) & (date < srs.loc['한로']):
            temp_year, temp_month = year, 8
        elif (srs.loc['한로'] <= date) & (date < srs.loc['입동']):
            temp_year, temp_month = year, 9
        elif (srs.loc['입동'] <= date) & (date < srs.loc['대설']):
            temp_year, temp_month = year, 10
        elif srs.loc['대설'] <= date:
            temp_year, temp_month = year, 11
    except:
        # we have no data if year < 1900 or 2050 < year
        temp_year, temp_month = year, month

    temp_year_result = __parse_year(temp_year)
    dict_month1 = {1:'갑', 2:'을', 3:'병', 4:'정', 5:'무', 6:'기', 7:'경', 8:'신', 9:'임', 0:'계'}
    dict_month2 = {11:'자', 12:'축', 1:'인', 2:'묘', 3:'진', 4:'사', 5:'오', 6:'미', 7:'신', 8:'유', 9:'술', 10:'해'}
    if temp_year_result[0] in ['갑', '기']:
        index_month1 = (temp_month + 2) % 10
    elif temp_year_result[0] in ['을', '경']:    
        index_month1 = (temp_month + 4) % 10
    elif temp_year_result[0] in ['병', '신']:
        index_month1 = (temp_month + 6) % 10
    elif temp_year_result[0] in ['정', '임']:
        index_month1 = (temp_month + 8) % 10
    elif temp_year_result[0] in ['무', '계']:
        index_month1 = temp_month % 10
    index_month2 = temp_month
    result_month = ''.join([dict_month1[index_month1], dict_month2[index_month2]])

    # parse date
    base_date = datetime.datetime(1900, 1, 1)
    input_date = datetime.datetime(year, month, day)
    diff = (input_date - base_date).days
    index_day1 = diff % 10
    index_day2 = diff % 12
    dict_day1 = {0:'갑', 1:'을', 2:'병', 3:'정', 4:'무', 5:'기', 6:'경', 7:'신', 8:'임', 9:'계'}
    dict_day2 = {0:'술', 1:'해', 2:'자', 3:'축', 4:'인', 5:'묘', 6:'진', 7:'사', 8:'오', 9:'미', 10:'신', 11:'유'}
    result_day = ''.join([dict_day1[index_day1], dict_day2[index_day2]])

    return ', '.join([result_year, result_month, result_day])

def element_count(gapja_string):
    '''
    input result from gapja_string to get dictionary of element counts.
    gapja_string : result of py48.parser.parse, e.g. '을해, 정해, 신해'
    return : e.g. {'화': 1, '수': 3, '목': 1, '금': 1, '토': 0}
    '''
    element_dict = {
        '자':'수', '축':'토', '인':'목', '묘':'목', '진':'토', '사':'화', '오':'화', '미':'토',
        '신':'금', '유':'금', '술':'토', '해':'수', '갑':'목', '을':'목', '병':'화',
        '정':'화', '무':'토', '기':'토', '경':'금', '신':'금', '임':'수', '계':'수'    
    }
    gapja_list = [element_dict[gapja_string[idx]] for idx in ([0, 1, 4, 5, 8, 9])]
    element_list = ['화', '수', '목', '금', '토']
    element_count = {element:gapja_list.count(element) for element in element_list}
    return element_count

__lunar_months_df = __load_df()
