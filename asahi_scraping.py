import requests
import sys
from bs4 import BeautifulSoup
import pandas as pd

################### Settings ###################

session_id = 'PUT YOUR SESSION ID HERE'
keyword = 'PUT YOUR KEYWORD HERE'
year_begin = 1984
year_end = 2019

################################################

base_url = 'https://database.asahi.com/'
cookie = {'PHPSESSID': session_id}
data_frame = []

def exitWithError(message, response = None):
    if response != None:
        print(response.text)
    sys.exit(message)

def search():
    url = base_url + 'library2/topic/t-list.php'
    total = 0;

    print('キーワード: ' + keyword + ' を含む記事の件数を抽出します')

    for current_year in range(year_begin, year_end+1):
        year = str(current_year)
        post_data = {
            'rdoSrchMode': '0',
            'chkShishi': 'N',
            'txtWord': keyword,
            'btnSearch': '検索実行',
            'hdnItaiji': '1',
            'hdnDougigo': '1',
            'rdoSrchTerm': '4',
            'cmbIDFy': year,
            'cmbIDFm': '01',
            'cmbIDFd': '01',
            'cmbIDDm': 'FROM',
            'cmbIDTy': year,
            'cmbIDTm': '12',
            'cmbIDTd': '31',
            'rdoSrchItem': 'MHK',
            'txtBunrui': '',
            'chkKan': 'M',
            'chkKan': 'E',
            'txtMenmei': '',
            'chkHochi': 'N',
            'chkHochi': 'L',
            'chkIssueS': 'T',
            'chkIssueS': 'O',
            'chkIssueS': 'N',
            'chkIssueS': 'S',
            'chkIssueS': 'H',
            'cmbDspNum': '20',
            'rdoDspOrder': 'NEW',
            'loginSID': session_id,
            'srchId': '12',
            'srchKind': 'zent',
            'selectNo': '',
            'kiriId': '',
            'cond': '2&3,ShishiName,1,N,HakkouDate,5,'+year+'0101:'+year+'1231',
            'ronri': '2&3',
            'hdnSrchMode': '0',
            'hdnShishi': 'N',
            'hdnShishiOrg': 'N',
            'hdnWord': keyword,
            'hdnKeyword': keyword,
            'hdnSrchTerm': '4',
            'hdnIssueDate': year+'0101:'+year+'1231',
            'hdnIDFy': year,
            'hdnIDFm': '01',
            'hdnIDFd': '01',
            'hdnIDDm': 'FROM',
            'hdnIDTy': year,
            'hdnIDTm': '12',
            'hdnIDTd': '31',
            'hdnSrchItem': 'MHK',
            'hdnBunrui': '',
            'hdnKan': '',
            'hdnKanOrg': 'M+E',
            'hdnMenmei': '',
            'hdnHochi': '',
            'hdnHochiOrg': 'N+L',
            'hdnIssueS': '',
            'hdnIssueSOrg': 'T+O+N+S+H',
            'hdnShaZuHyo': '',
            'hdnShaZuHyoOrg': '',
            'hdnDspNum': '20',
            'hdnDspOrder': 'NEW',
            'hdnDispSoukensuOnlyFlag': '0',
            'hdnSrchStart': '',
            'hdnSrchEnd': '',
            'hdnAsahi': 'Y',
            'hdnAera': 'Y',
            'hdnWeekly': 'Y',
            'genre_pos': '',
            'saveSelectGenre': '',
            'saveSearchMode': '0',
            'txtLogKW': '',
            'hdnSaisingou': '',
            'txtOudanWord': '',
            'hdnOudanKeyword': '',
            'data_asahi': '',
            'data_shimen_meiji': '',
            'data_shimen_senzen': '',
            'data_shimen_sengo': '',
            'data_shimen_heisei': '',
            'data_chiezo': '',
            'data_jinbutu': '',
            'data_graph': ''
        }

        response = requests.post(url, data=post_data, cookies=cookie)

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('title').text == '認証エラー':
            exitWithError('認証エラーが発生しました。セッションIDをセットしましたか?')

        count = int(soup.find('input', {'name': 'hdnOut_List_HitListCount'}).get('value'))

        print(year + ':' + str(count))
        total += count

        data_frame.append([year, count])

    print('記事の合計件数: ' + str(total) + '件')

def write_csv():
    file_name = keyword + '_' + str(year_begin) + '_' + str(year_end) + '.csv'
    df = pd.DataFrame(data_frame, columns=['year', 'count'])
    df.to_csv(file_name)
    print('CSVファイルを以下のファイル名で出力しました: ' + file_name)

if __name__ == "__main__":
    search()
    write_csv()
