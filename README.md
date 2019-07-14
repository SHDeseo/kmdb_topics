<h2 id="section"><img src="https://lh6.googleusercontent.com/MVkZAVCNaQji-z3k_8UAgt471Al432p1ewmn_By0hPE8s71_7__zpywEl8PidCpCMHG1LaWfNizPzUVdJ4K41PY9E_EvU3MbmN4vXRmAFW9BZBwFubx1nHJ_cvUr7CWaQE5ehUWY" alt="" title="가로선"></h2>
<p><img src="https://lh6.googleusercontent.com/Psup8v-tDOvf_byOw9bfQ1b_QPpEnteRsSczXs-i1jUHoRIF9KVudx5SfLZiciUzjXqEGC6WhdXFA2Zlfof5Q-wAsHl-ETqRjOY1M7tYnIpu8O5fVFvM16gqF0KtVmlK4z34lMCu" alt="" title="자리표시자 이미지"></p>
<p>Topic Model을 이용한 한국고전영화 추천 시스템</p>
<p>2018년 11월 26일</p>
<h1 id="개요">개요</h1>
<p>한국영상자료원이 운영하는 한국영화데이터베이스(KMDb)에서 최근 한국고전영화 VOD 서비스를 전면 무료로 전환했다. 하지만 90년대 이전에 제작된 한국영화는 젊은 이용자들에게는 낯설다. 일부 영화의 상세정보에는 영자원의 관리자에 의한 키워드, 장르 정보가 제공되며 전문가들이 정리한 시놉시스도 제공된다. 이를 이용해 아이템 중심의 추천시스템을 개발한다면 이용자들이 더 용이하게 작품을 브라우징할 수 있어 접근성이 증대될 것으로 예상된다. 아직 영화에 대한 이용자들의 평점 정보가 없는 상황에서 영화상세정보의 키워드, 장르, 시놉시스를 Topic Model로 분석, 유사한 소재와 주제를 가진 영화들을 묶어 추천해줄 수 있을 것이다.</p>
<h1 id="목표">목표</h1>
<ol>
<li>
<p>1999년 이전에 한국에서 제작된 극영화, 애니메이션, 다큐멘터리 영화의 상세정보를 KMDb 영화상세정보 API로 수집, 잠재 디리클레 할당(LDA)으로 내용적으로 관련이 있는 영화를 묶어줄 topic을 추출한다.</p>
</li>
<li>
<p>특정 고전영화의 영화제목과 개봉년도를 “{영화제목}, {개봉년도}” 의 형식으로 입력 받아 같은 topic을 가진 고전영화 10개의 간략한 정보와 vod 서비스 링크를 출력한다.</p>
</li>
</ol>
<h1 id="데이터-설명">데이터 설명</h1>
<p>1999년 이전에 한국에서 제작된 극영화, 애니메이션, 다큐멘터리 영화 6504편의 영화 상세정보.</p>
<ul>
<li>데이터 수</li>
</ul>

<table>
<thead>
<tr>
<th>극영화</th>
<th>애니메이션</th>
<th>다큐멘터리</th>
<th>총계</th>
</tr>
</thead>
<tbody>
<tr>
<td>5860</td>
<td>363</td>
<td>281</td>
<td>6504</td>
</tr>
</tbody>
</table><ul>
<li>변수</li>
</ul>

<table>
<thead>
<tr>
<th>변수명</th>
<th>설명</th>
<th>데이터형</th>
</tr>
</thead>
<tbody>
<tr>
<td>movieId</td>
<td>영화 고유 Id</td>
<td>한 자리 문자열 (ex. ‘A’, ‘K’)</td>
</tr>
<tr>
<td>movieSeq</td>
<td>등록Seq (Id와 결합되는 고유값)</td>
<td>숫자로 이루어진 5자리 문자열</td>
</tr>
<tr>
<td>title</td>
<td>제목</td>
<td>문자열</td>
</tr>
<tr>
<td>year</td>
<td>제작년도</td>
<td>정수</td>
</tr>
<tr>
<td>genre</td>
<td>장르</td>
<td>문자열</td>
</tr>
<tr>
<td>keywords</td>
<td>키워드</td>
<td>문자열</td>
</tr>
<tr>
<td>genre</td>
<td>장르</td>
<td>문자열</td>
</tr>
<tr>
<td>plot</td>
<td>줄거리</td>
<td>문자열</td>
</tr>
</tbody>
</table><h1 id="마일스톤">마일스톤</h1>
<h2 id="kmdb-영화상세정보-api를-이용한-데이터-수집-11.04--11.21">1. KMDb 영화상세정보 API를 이용한 데이터 수집 (11.04 ~ 11.21)</h2>
<p>JSON 출력값을 불러오는 API를 이용해 총 6504편의 영화 상세정보를 수집.</p>
<h2 id="잠재-디리클레-할당lda-방식을-이용한-topic-추출-11.25-">2. 잠재 디리클레 할당(LDA) 방식을 이용한 topic 추출 (11.25 ~)</h2>
<p>가장 정확하게 유관한 영화들을 묶어줄 최적의 topic수를 탐색.</p>
<p><img src="https://lh6.googleusercontent.com/QLS_6sNLUmHextJO4dPaXDmq_LvQWFjCasqMvQZWFFUqOdpnvLaQdzcCm8O-7hmWOLkUNROYQln3qL7hcV41tmGhJNu3vSk2NL3aA4fcZu4dhx5Ie36KrNA7SU2tM3wzoH_9CcR1" alt=""></p>
<p>topic 수에 따른 모델의 성적<img src="https://lh4.googleusercontent.com/tfFsiJdTD2FEfrt646Ydfb_AOGKbQbLBTyI5N_QkPWKB7tpzCgtadvIjFOJLZKA9xVLCNaykraEhGNVBq7cduup8mvTov9ZNG1KHpianxckelOsqR0X8laqThnSZIIrplWN6Qtr6" alt=""></p>
<p><strong><img src="https://lh4.googleusercontent.com/tfFsiJdTD2FEfrt646Ydfb_AOGKbQbLBTyI5N_QkPWKB7tpzCgtadvIjFOJLZKA9xVLCNaykraEhGNVBq7cduup8mvTov9ZNG1KHpianxckelOsqR0X8laqThnSZIIrplWN6Qtr6" alt=""></strong></p>
<p>topic 별 주요단어</p>
<p><img src="https://lh5.googleusercontent.com/Uq6ou9XvqeYjTHz9B0hY0A00IjcEOGQ-CpGKupd2PCsMYJSFQoP4CTZGcksXFQP2KNwxiCSRmw85Q_RGHi9AyuW0Nbvhlogbil_KbsxJB2DY_wyhlIO4bIT7Q9w_QYxsy35tlhBI" alt=""></p>
<p>2차원으로 나타낸 토픽 별 영화의 분포</p>
<h2 id="입력값을-받아-관련-topic을-가진-영화-10개를-출력">3. 입력값을 받아 관련 topic을 가진 영화 10개를 출력</h2>
<p>영화의 줄거리, 장르, 키워드 안에 내재되어있을 것으로 예상되는 토픽들의 할당 확률이 유사한 두 영화는 주제적으로 유사하다고 가정, 할당 확률을 코사인 유사도로 유사성을 평가해 가장 유사한 10개의 영화를 출력해 보여준다.</p>
<h2 id="flask-웹-게시">flask 웹 게시</h2>
<p>준비 중</p>

