<h1 id="kmdb-api-with-python--request">KMDb API with Python &amp; Request</h1>
<h5 id="section">2018.11.04</h5>
<p>KMDb API 코드예시에 파이썬이 없어서 쓰는 글 (겸 프로젝트 일지).<br>
목표는 KMDb에서 제공하는 영화상세정보 API로 1999년까지 한국에서 제작/개봉한 극영화,다큐멘터리,애니메이션을 포함한 6493편의 영화의 상세정보(제목, 개봉년도, 제작사, 주요 크레딧, 줄거리 등)을 수집해 LDA로 토픽 추출을 하는 것이다. <s>이 프로젝트를 하는 이유는 일부 이용자와 관리자가 부여하는 키워드에 한계를 느꼈고 한국고전영화에 대한 일반 대중의 접근성 증대, 아이템 기반의 추천시스템 개발의 밑거름? 을 하고 싶어서임.</s></p>
<p>글을 쓰는 이유는 KMDb API 이용안내에 코드예시가 Java, JS, PHP밖에 없어서 일반적으로 비전문가가 접근하기 쉬운 Python으로 된 사용기를 남기고 싶어서 기록하게 되었다. (=Requests 배운지 너무 오래되어서 복기할 목적이다)</p>
<p>서문이 길었네요…<br>
암튼 JS 샘플코드를 좀 분석해봤는데 url에 queryparam을 붙여서 리퀘스트용 url을 만들어서 get으로 정보를 가져오면 되는 거 같구. queryparam은 <a href="https://www.kmdb.or.kr/info/api/apiDetail/6">요청인자</a>로 이루어져있고.<br>
샘플코드에는 url과 query사이에 <code>?</code>를 추가하고 query의 요소 사이에 <code>&amp;</code>를 일일히 더해주는 코드를 써서  url을 만드는데 이건 BeautifulSoup의 <code>get</code>의 파라미터 <code>params</code>가 생성해준다. <code>params</code>는 key에 컴포넌트, value에 질의내용이 들어간 딕셔너리를 받는다.</p>
<pre><code>&gt;&gt; payload = {'key1': 'value1', 'key2': 'value2'}
&gt;&gt; r = requests.get('https://httpbin.org/get', params=payload)
&gt;&gt; print(r.url)
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
<hr class="footnotes-sep">
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1" class="footnote-item"><p>‘REST API 제대로 알고 사용하기’ <a href="https://meetup.toast.com/posts/92">https://meetup.toast.com/posts/92</a> <a href="#fnref1" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn2" class="footnote-item"><p>‘HTTP / RESTful API Calls with Python Requests Library’ <a href="https://techietweak.wordpress.com/2015/03/30/http-restful-api-with-python-requests-library/">https://techietweak.wordpress.com/2015/03/30/http-restful-api-with-python-requests-library/</a> <a href="#fnref2" class="footnote-backref">↩︎</a></p>
</li>
</ol>
</section>

