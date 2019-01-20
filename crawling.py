import numpy as np
import pandas as pd
from tqdm import tqdm_notebook
import requests
import json
from bs4 import BeautifulSoup
import pickle

f = open('mykey.plk', 'rb')
mykey = pickle.load(f)

url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?\
collection=kmdb_new&detail=Y&ServiceKey='+mykey

profiles = pd.DataFrame(columns=['movieId','movieSeq','title','year','director','directorId','writer','writerId','actors','actorId','pd','genre','keywords','plot'])

guide = 'https://www.kmdb.or.kr/info/api/apiDetail/6'
response = requests.get(guide)

# http://toughbear.tistory.com/entry/python-args%EC%99%80-kwargs-%EC%9D%98%EB%AF%B8%EC%99%80-%EC%82%AC%EC%9A%A9
def getClean(content):

    """
    문법적 오류로 인해 str으로 처리되는 requests 의 response.content를
    문법적으로 틀린 부분을 수정한 JSON으로 바꿔줍니다.
    """

    """
    1. KMDb API의 JSON 출력값을 str으로 변환, 공백 삭제 후 불필요한 어레이([])를 제거합니다
    """

    raw = content.decode('utf-8').strip()
    left = raw.find('"Data":') + len('"Data":')
    result = raw[:left] + raw[left+1:-3] + raw[-1:]

    """
    2. extra comma를 제거합니다
    """

    errordict = {
        ',}':'}',
        ',]':']',
        ', }' : '}',
        ', ]' : ']',
        '} {' : '}, {',
        '] [' : '], [',
        '}{' : '}, {',
        '][' : '], ['
    }


    for case in errordict.keys() :

        while result.find(case) != -1:
            result = result.replace(case,errordict[case])

    try :
        json.loads(result)
    except:
        if result[-4:] != '}]}}':
            result  = result +'}'



    return json.loads(result)

def json_to_dF(response_info, dataFrame):

    df = dataFrame.copy()

    for idx in range(len(response_info['Data']['Result'])):
        row = response_info['Data']['Result'][idx]

        drct = ''
        drctId= ''
        for dr in row['director']:
            drctId += dr['directorId'] + ','
            drct += dr['directorNm']+','

        acts = ''
        actsId = ''
        for act in row['actor']:
            actsId += act['actorId']+','
            acts += act['actorNm']+','

        writerNm = [staff['staffNm'] for staff in row['staff'] if staff['staffRoleGroup'] == '각본']
        writerId_ls = [staff['staffId'] for staff in row['staff'] if staff['staffRoleGroup'] == '각본']




        df.loc[idx] = {
            'movieId': row['movieId'],
            'movieSeq': row['movieSeq'],
            'title': row['title'].strip(),
            'year': row['prodYear'].strip(),
            'pd': row['company'].strip(),
            'plot': row['plot'].strip() ,
            'genre': row['genre'].strip() ,
            'keywords': row['keywords'].strip(),
            'director': drct,
            'directorId': drctId,
            'writer': ','.join(writerNm),
            'writerId' : ','.join(writerId_ls),
            'actors': acts,
            'actorId': actsId,
        }

        df.replace(to_replace='',value=',', inplace=True)

    return df

class getProfiles:
    """
    리퀘스트문 날리는 class

    url: 기본 url + key + 기본적인 쿼리(ex. 'details=Y')
    queryDict: dictionary. key = 요청인자, value = 검색어 ex) 'createDts' : '1991'.
    profiles_df: Df. jason_to_df 와 동일한 columns을 가지고 있어야 함.

    """

    def __init__(self, url, queryDict, profiles_df):

        self.url = url
        self.queryDict = queryDict
        self.pframe = profiles_df


    def crawling(self):

        query = self.queryDict.copy()

        q1 = {
            'details':'N',
           'listCount':'1',
            'type' :  self.queryDict['type']
        }
        query.update(q1)

        response = requests.get(url, query)
        info = getClean(response.content )

        totalcnt = info['TotalCount']

        errorspaces = []
        result_df = self.pframe.copy()
        query = self.queryDict.copy()
        listcnt = query['listCount']

        print('Movie type is ', self.queryDict['type'])
        print('Starts crawling ', totalcnt,'titles...')

        if totalcnt < listcnt:
            itr = {
                'listCount' : totalcnt
            }

            query.update(itr)
            response = requests.get(self.url, query)

            try:
                result = json_to_dF(dataFrame = self.pframe, response_info = getClean(response.content))
                result_df = pd.concat([result_df, result]).reset_index(drop=True)

            except:
                print(startrow,'~',startrow+listcnt,'has bean passed...')
                errorspaces.append((startrow,startrow+listcnt))

        else:
            iteration = np.arange(0,totalcnt, listcnt)


            for startrow in tqdm_notebook(iteration):

                itr = {
                'listCount' : listcnt,
                'startCount' : startrow,
                }

                query.update(itr)

                response = requests.get(self.url, query)

                try:
                    result = json_to_dF(dataFrame = self.pframe, response_info = getClean(response.content))
                    result_df = pd.concat([result_df, result]).reset_index(drop=True)


                except:
                    print(startrow,'~',startrow+listcnt,'skipped...')
                    errorspaces.append((startrow,startrow+listcnt))
        print(len(result_df),' titles have been collected.')

        if len(errorspaces) == 0:
            print('No errors occured.')
            print('\n')

        else:
            print('Finding where error(s) occured...')
            # 에러 구간 errorspaces 에서 에러를 일으키는 타겟targets을 찾는다.


            targets = []

            def finderror(start, cnt):

                itr = {
                    'details' : 'N',
                    'startCount' : start,
                    'listCount': cnt,
                }
                query.update(itr)
                response = requests.get(self.url, query)

                if 'error' in response.content.decode('utf-8'):
                    return 1
                else:
                    return 0

            targets = []

            for space in errorspaces:
                start = space[0]
                cnt = listcnt

                workstack = []

                while True:
                    cnt = (cnt+1)//2

                    if finderror(start,cnt) == 0:
                        start += cnt

                    if finderror(start, cnt) == 1:
                        if finderror(start+cnt, cnt) == 1:
                            workstack.append((start+cnt, cnt))

                        else:
                            pass

                        if cnt == 1:
                            targets.append(start)
                            print('An error found...')

                            if len(workstack) == 0:
                                break
                            else:
                                (start, cnt) = workstack.pop(-1)
                        else:
                            pass

                    else:
                        if finderror(start+cnt, cnt) == 1:
                            start = start+cnt

                            continue
                        else:
                            print('No errors occured.')
                            break
            print(len(targets),' rows occured error.')


            self.targets = targets


            print('\n')
            print('Crawling avoiding errors...')
            errors = 0
            ranges = []
            for s in errorspaces:
                ranges.append([s[0]-1]+[t for t in targets if t>s[0] and t<s[1] ]+[s[1]])

            for space in ranges:
                for idx in range(len(space)-1):
                    listcnt = space[idx+1] - space[idx]-1
                    startrow = space[idx]+1
                    print("Getting from ",startrow,'to',space[idx+1]-1)

                    itr = {
                        'details' : 'Y',
                        'listCount' : listcnt,
                        'startCount' : startrow,
                    }

                    query.update(itr)
                    response = requests.get(self.url, query)
                    info = getClean(response.content)
                    df = json_to_dF(dataFrame = self.pframe, response_info = info)
                    errors += len(df)
                    result_df = pd.concat([result_df, df]).reset_index(drop=True)

            print('\n')
            print(errors,' titles has been added.')
            print(len(result_df),' titles have been collected.')



        print('Crawling finished.')
        return result_df

cinema_q = {
    'details':'Y',
    'nation':'대한민국',
    'createDts':'0',
    'createDte':'1999',
    'listCount' : 120,
    'startCount' : 0,
    'type' : '극영화',
}

cinema = getProfiles(url, cinema_q, frame)
profiles_cinema = cinema.crawling()
print('--------------------------------------------------')


docuq = {
    'details':'Y',
    'nation':'대한민국',
    'createDts':'0',
    'createDte':'1999',
    'listCount' : 250,
    'startCount' : 0,
    'type' : '다큐멘터리',
}

docu = getProfiles(url, docuq, frame)
profiles_docu = docu.crawling()
print('--------------------------------------------------')


animeq = {
    'details':'Y',
    'nation':'대한민국',
    'createDts':'0',
    'createDte':'1999',
    'listCount' : 250,
    'startCount' : 0,
    'type' : '애니메이션',
}

anime = getProfiles(url, animeq, frame)
profiles_anime = anime.crawling()


whole_profiles = pd.concat([profiles_cinema, profiles_anime, profiles_docu]).reset_index(drop=True)

print('whole profiles shape :', whole_profiles.shape)
filepath = 'data/profiles.csv'
try:
    whole_profiles.to_csv(filepath, index=False)
except:
    !mkdir data
    whole_profiles.to_csv(filepath, index=False)
print('Exported as ',filepath)
