<h1 id="kmdb-api-with-python--request">KMDb API with Python &amp; Request</h1>
<h5 id="section">2018.11.04</h5>
<p>KMDb API 코드예시에 파이썬이 없어서 쓰는 글 (겸 프로젝트 일지).<br>
목표는 KMDb에서 제공하는 영화상세정보 API로 1999년까지 한국에서 제작/개봉한 극영화,다큐멘터리,애니메이션을 포함한 <s>6493</s> 6394편의 영화의 상세정보(제목, 개봉년도, 제작사, 주요 크레딧, 줄거리 등)을 수집해 LDA로 토픽 추출을 하는 것이다. <s>이 프로젝트를 하는 이유는 일부 이용자와 관리자가 부여하는 키워드에 한계를 느꼈고 한국고전영화에 대한 일반 대중의 접근성 증대, 아이템 기반의 추천시스템 개발의 밑거름? 을 하고 싶어서임.</s></p>
<p>글을 쓰는 이유는 KMDb API 이용안내에 코드예시가 Java, JS, PHP밖에 없어서 일반적으로 비전문가가 접근하기 쉬운 Python으로 된 사용기를 남기고 싶어서 기록하게 되었다. (=Requests 배운지 너무 오래되어서 복기할 목적이다)</p>
<p>서문이 길었네요…<br>
암튼 JS 샘플코드를 좀 분석해봤는데 url에 queryparam을 붙여서 리퀘스트용 url을 만들어서 get으로 정보를 가져오면 되는 거 같구. queryparam은 <a href="https://www.kmdb.or.kr/info/api/apiDetail/6">요청인자</a>로 이루어져있고.<br>
샘플코드에는 url과 query사이에 <code>?</code>를 추가하고 query의 요소 사이에 <code>&amp;</code>를 일일히 더해주는 코드를 써서  url을 만드는데 이건 BeautifulSoup의 <code>get</code>의 파라미터 <code>params</code>가 생성해준다. <code>params</code>는 key에 컴포넌트, value에 질의내용이 들어간 딕셔너리를 받는다.</p>
<pre><code>payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)

[out]: https://httpbin.org/get?key2=value2&amp;key1=value1
</code></pre>
<p>여기까지 했는데 <code>ERR-300</code> 이 반복된다. 빠진 요소가 있다는 것인데.<br>
<br><br><br>
뭐가 문제일까 싶어서 API 이용안내를 다시 보는데 <strong>REST</strong> 방식이라는게 뒤늦게 눈에 띈다. REST? 그냥 리퀘 날리면 되는거 아냐?</p>
<pre><code>영화상세정보를 영화명, 감독, 키워드 등의 요청값을 통해 조회합니다.  
호출방식은 REST, 응답형식은 XML과 JSON을 지원합니다.  

기본 요청
URL : https://kmdb.or.kr/info/api/6/api.xml (또는 .json)
</code></pre>
<p><br><br><br>
위의 기본요청 URL로 아무리 리퀘를 날려도 안 되길래 JS 샘플코드를 참고했다. 거기엔 이런 URL이 기본으로 쓰이고 있다.<br>
<code>http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?collection=kmdb_new&amp;nation=대한민국</code></p>
<p>???<br>
<code>?</code> 뒤를 요청인자라고 보더라도 기본요청의 URL과 너무 다른데?</p>
<p>혹시몰라서 위 URL을 가지고 리퀘를 날려봤다.</p>
<blockquote>
<p>결과리스트 갯수 : 1<br>
제작년도시작: 1998<br>
제작년도끝: 1999<br>
국가: 한국<br>
collection=kmdb_new (고정값)</p>
</blockquote>
<pre class=" language-python"><code class="prism  language-python">sample<span class="token operator">=</span><span class="token string">'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp'</span>
sampleresponse <span class="token operator">=</span> requests<span class="token punctuation">.</span>get<span class="token punctuation">(</span>sample<span class="token punctuation">,</span> q1<span class="token punctuation">)</span>
sample_info <span class="token operator">=</span> sampleresponse<span class="token punctuation">.</span>content
sampleresponse<span class="token punctuation">.</span>url
<span class="token operator">&gt;&gt;</span><span class="token string">'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?ServiceKey=서비스키&amp;listCount=1&amp;collection=kmdb_new&amp;createDts=1998&amp;createDte=1999&amp;nation=%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD'</span>
</code></pre>
<p>뭔가 오긴 왔는데 utf-8로 인코딩된 바이너리 데이터다.<br>
<img src="https://lh3.googleusercontent.com/e09T9dQ81JaySl0MtYdtH_Uo1Sxh2FNB0L5kwOf1SUBIahAQFhxvG4SkqQWY2RwedBYfSjyWeeAN" alt="" title="bi"></p>
<p><code>json.load()</code> 도 이용할 수 없다. 바이너리니까.</p>
<p>REST API 방식은 resource와 resource에 대한 method가 표현된다고 하는데<sup class="footnote-ref"><a href="#fn1" id="fnref1">1</a></sup> , 샘플코드나 요청인자 테이블에 관련된 설명은 없고. 뭔지모르겠는데/??</p>
<p>Requests라이브러리와 REST API를 연결해 설명해주는 이 블로그에 따르면<sup class="footnote-ref"><a href="#fn2" id="fnref2">2</a></sup> <code>GET</code>을 수행할 때, 때에 따라서 다음과 같은 파라미터가 필요하다.</p>
<ol>
<li>url</li>
<li>header</li>
<li>params</li>
<li>auth</li>
</ol>
<p>샘플코드에서는 여기서 url과 params만 사용하고 있다.<br>
그리고 샘플코드의 출력값은 인수가 59개인데 샘플코드의 결과값은 15개밖에 안된다…<br>
그런데 이 샘플코드의 url를 사용하는 깃헙을 발견해서 링크를 가져와봤더니 결과는 잘 나온다. 근데… 좀 께림직하다.</p>
<p><code>http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_xml.jsp?collection=kmdb_new&amp;ServiceKey=서비스키&amp;director=%EC%9A%B0%EB%94%94%EC%95%A8%EB%9F%B0&amp;startCount=0&amp;listCount=100&amp;sort=prodYear,1</code></p>
<p>끝에 <code>1</code>은 왜 붙이죠?..</p>
<p><code>http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?collection=kmdb_new&amp;ServiceKey=서비스키&amp;director=%EC%9A%B0%EB%94%94%EC%95%A8%EB%9F%B0&amp;startCount=0&amp;listCount=100&amp;sort=prodYear</code></p>
<p>json일 때에는 <code>1</code>을 안붙이죠? 그리고 결과는 왜 바이너리죠?</p>
<h1 id="section-1"></h1>
<h5 id="section-2">11.05</h5>
<p><img src="https://lh3.googleusercontent.com/cnuT34vsFvUonba0Sm3Sg9pyMwpgQZHnN2Oe-EWgM_IOxcCzoej5lzRr_7JseYx43VrQ-6Gr-m6P=s1000" alt=""></p>
<p><code>http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?collection=kmdb_new&amp;detail=N&amp;director=%EB%B0%95%EC%B0%AC%EC%9A%B1&amp;ServiceKey=키값</code></p>
<p>이 URL은 <code>detail(상세정보 출력여부)=N, dircetor=박찬욱</code> 으로 요청하는 것이었다. 바이너리 포맷의 제이슨이 성공적으로 출력된다.</p>
<p>문제는 이 제이슨을 제이슨 형태로 바꿀 수 없다는 것이다. 아마도 제이슨 문법을 따르지 않는 형태로 전송된 것 같다.<br>
이번 기회에 api를 이용해 xml 출력값 처리하는 방법을 공부해보는 것도 좋을듯. 오늘은 말고…</p>
<h1 id="section-3"></h1>
<h4 id="section-4">11.12</h4>
<p>출력값에서 JSONEncoder 오류를 일으키는 부분을 찾아냈다. <code>[]</code> 어레이가  <code>,</code> 구분자로 끝나서 생긴 오류였다. 애초에 값이 하나의 오브젝트만 들어가는 어레이였기 때문에 일단 <code>[]</code>와 해당 콤마를 없앴더니 바이너리를 인코딩한 스트링에서 문제 없이 json으로 변환되었다… 아… 막연하게 문법을 지키지 않은 데이터라서 어디서부터 고쳐야할 지 막막했는데 정상적인 JSON데이터 보면서 살짝 만져봤더니 해결되버린다.</p>
<h1 id="section-5"></h1>
<h4 id="section-6">11.18</h4>
<p>extra comma는 흔한 JSON 에러였다는걸 JSON 구문에서 오류를 찾아주는 툴(<a href="https://jsonlint.com/">https://jsonlint.com/</a>)의 도움이 빌려서 알게 되었다.</p>
<blockquote>
<ul>
<li>Expecting  <code>'STRING'</code>  - You probably have an extra comma at the end of your collection. Something like  <code>{ "a": "b", }</code></li>
<li>Expecting  <code>'STRING'</code>,  <code>'NUMBER'</code>,  <code>'NULL'</code>,  <code>'TRUE'</code>,  <code>'FALSE'</code>,  <code>'{'</code>,  <code>'['</code>  - You probably have an extra comma at the end of your list. Something like:  <code>["a", "b", ]</code></li>
</ul>
</blockquote>
<p>출력결과의 갯수를 늘렸더니 같은 에러가 반복되었다. 이는 어레이 리스트나 콜렉션을 닫는 }나 ] 앞에 불필요한 <code>,</code>가 붙는 extra comma 에러가 출력값 중간중간에도 발생한다는 뜻이다. KMDb의 JSON 출력값에 생각보다 에러가 많지만 언제나 깔끔하게 정리된 데이터만 받아서 쓸 수는 없을테니까 이렇게 에러가 있는 데이터를 정돈해 쓰는 것도 좋은 경험이라고 생각한다.<br>
JSON 정제 끝.<br>
<br><br></p>
<h3 id="출력값의-문제.">출력값의 문제.</h3>
<p>KMDb 영화상세정보 API는 xml 과 json 두 가지 언어로 제공되는데 xml에는 있지만 json에는 없는 출력값 요소가 있다.</p>

<table>
<thead>
<tr>
<th></th>
<th>요청인자</th>
<th></th>
<th>출력결과</th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td>startCount</td>
<td>출력결과의 시작점</td>
<td>PageNo</td>
<td>검색결과 중 노출되는 시작점</td>
</tr>
<tr>
<td></td>
<td>listCount</td>
<td>출력결과 갯수</td>
<td>NumOfRow</td>
<td>한 페이지당 출력 결과</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table><p>xml의 경우</p>
<pre><code>listCount=20&amp;startCount=20
</code></pre>
<p>으로 설정하면 <strong>20번째 출력결과에서 부터 20개가 출력</strong>되며 pageNo와 NumOfRow 라는 파라미터가 이를 알려준다.<br>
json 출력값에는 이 두 파라미터가 생략되어있다.<br>
…?!<br>
<code>listCount=1000</code>으로 놓았을 때 row가 258개까지 불러오는 걸 보아서 json에서 listCount의 최대값은 258인 듯 하다. 아마도 나처럼 크롤링을 위해서라기 보다는 검색결과를 보여주기 위해서 사용되기 때문에 최대값을 정해놓은 것일테다. 그럼에도 일단 안내 페이지에 정보가 너무 부족하다는건 확실함.<br>
이 시점에서 차라리 미리 json 파일로 만들어 놓은 전체 DB를 사용하면 어떨가 하는 생각이 들었는데 내가 원하는 ‘키워드’ ‘장르’ ‘줄거리’ 는 제공되지 않기 때문에 결국 api를 사용할 수 밖에 없다.<br>
결국 json을 계속 사용한다면250개씩 분절된 정보를 5749/250 = 약 23회 가져오는 수 밖에 없다. xml 파싱하는 라이브러리 진작 공부해 둘 걸.</p>
<h1 id="section-7"></h1>
<h4 id="section-8">11.21</h4>
<p>for문으로 23회에 걸쳐 데이터를 가져오는건 문제가 아니었다. 불러온 출력값에 에러를 일으키는 결과가 있어서 에러를 알리는 경고문만 출력되었다. listCount의 최소값이 3인 덕분에 3개씩 불러와서 에러를 일으키는 결과 row가 무엇인지 찾아내고 그걸 피해서 결과를 가져오는 작업을 했다. 삽질 같지만 별로 어렵지 않다. 데이터 전처리가 좀 잘 맞는 것 같기도 하다.</p>

<table>
<thead>
<tr>
<th></th>
<th>극영화</th>
<th>에니메이션</th>
<th>다큐멘터리</th>
</tr>
</thead>
<tbody>
<tr>
<td>총 검색결과</td>
<td>5864</td>
<td>364</td>
<td>281</td>
</tr>
<tr>
<td>불러드린 결과</td>
<td>5860</td>
<td>363</td>
<td>281</td>
</tr>
</tbody>
</table><p>총 <strong>6504</strong> 편의 영화정보를 수집했고 shape은 6504x14이다.<br>
csv에 저장했다.</p>
<h1 id="section-9"></h1>
<p>11.25<br>
LDA로 토픽을 뽑아내야 하는데 그리드 서치를 하는 방법을 찾아보고 있다. LDA는 sklearn라이브러리를 이용하고 그리드 서치하는 방식은 여기(<a href="https://www.machinelearningplus.com/nlp/topic-modeling-python-sklearn-examples/">how to grid search best topic models</a>)를 참고할 것이지만 아마 옛날 버전의 sklearn을 사용하는 것 같아서 그대로 따라하지는 않을 것이다.</p>
<p>파라미터를 어떻게 조정해야 할까 고민되는데 이 글에서는 하이퍼 파라미터는 조정하지 않고 최적의 topic수와 learning decay를 찾는 방법만 소개하고 있다.</p>
<p>sklearn LDA 모델에는 디리클레 분포를 따르는 하이퍼 파라미터가 두 개 있는데 <code>alpha</code>로 불리는 <strong>doc_topic_prior</strong>, <code>beta</code>로 불리는 <strong>topic_word_prior</strong>이다. alpha는 디리클레 분포의 peakiness를 조정하는 계수인데 이 값이 작을 수록 peakiness가 강해진다.  alpha가 LDA 모델에서 하는 역할은 각 문서가 특정 토픽에 할당될 확률 간의 차이를 좁히거나 늘리는 것이다. doc_topic_prior가 0에 가까울 수록 어느 하나의 토픽에 할당될 확률이 크게 두드러진다.<br>
<img src="http://i.imgur.com/zgXrEKI.png" alt=""><br>
출처:  <a href="https://ratsgo.github.io/from%20frequency%20to%20semantics/2017/06/01/LDA/">rat’s go - Topic Modeling, LDA</a></p>
<p>beta는 각 단어가 해당 토픽에서 나타날 확률에서 alph와 비슷한 역할을 한다고 한다.</p>
<p>그러니까 두 파라메터의 값에 따라 특정 토픽으로 할당될 확률이 도미넌트 해진다는 것인데 그냥 defaut인 <code>1/토픽수</code> 대로 써야할지 아니면 다른 식으로 조정하면 좋을지 잘 모르겠다.</p>
<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1" class="footnote-item"><p>‘REST API 제대로 알고 사용하기’ <a href="https://meetup.toast.com/posts/92">https://meetup.toast.com/posts/92</a> <a href="#fnref1" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn2" class="footnote-item"><p>‘HTTP / RESTful API Calls with Python Requests Library’ <a href="https://techietweak.wordpress.com/2015/03/30/http-restful-api-with-python-requests-library/">https://techietweak.wordpress.com/2015/03/30/http-restful-api-with-python-requests-library/</a> <a href="#fnref2" class="footnote-backref">↩︎</a></p>
</li>
</ol>
</section>

