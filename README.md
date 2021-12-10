# actions
spaceone github action workflow 저장소

+ 2021/12/10 plugin 구현

## 개요
공통적으로 사용되는 github action workflow를 저장/관리한다.<br>
각 repository에서 github action이 실행되면, 이 저장소에서 최신 상태의 workflow를 가져온 후 CI를 수행한다.

<img src = "https://user-images.githubusercontent.com/19552819/145518532-46ae01d4-5c23-4890-93f1-5b858c90cacf.png" width="80%" height="80%">
1. plugin_xxx repository에서 github action trigger 발생<br>
2. sync CI는 actions로 workflow를 요청한다<br>
3. actions는 python script를 실행하여 요청한 repository에 알맞은 workflow를 찾는다<br>
&nbsp;&nbsp;3-1. 이때, 해당 repository에 등록된 topic을 참고한다.(즉, 사전에 topic 설정이 필요하다.)<br>
4. workflow를 찾으면 요청한 repository에 workflow를 commit(Create or Update)한다.<br>
5. commit된 workflow를 trigger 한다.<br>
6. image를 build하여 docker hub에 push한다.


### workflow 추가
각 group의 workflows에 추가하고 싶은 workflow 파일을 추가해둔다.<br>
추후 deploy workflow가 동작하면서, 새롭게 추가된 파일을 지정 repository에 추가해준다.
```
├── README.md
├── backend
│   └── workflows     
│       └── new.yaml    ★ 이곳
├── plugin
│   └── workflows     
│       └── new.yaml    ★ 이곳
├── requirements.txt
├── src
│   ├── main.py
│   └── module
```
