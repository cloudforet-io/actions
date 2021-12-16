# actions
spaceone github action workflow 저장소

+ 2021/12/10 plugin 구현
+ 2021/12/16 init deploy 구현

## 개요
공통적으로 사용되는 github action workflow를 저장/관리한다.<br>
각 repository는 github action이 실행되면, 이 저장소에서 최신 상태의 workflow를 가져온 후 CI를 수행한다.

<img src = "https://user-images.githubusercontent.com/19552819/145733993-a055947b-ee08-462f-ab9e-340cc47b0c4a.png" width="80%" height="80%">
1. plugin_xxx repository에서 github action trigger 발생<br>
2. sync CI는 actions로 workflow를 요청한다<br>
3. actions는 python script를 실행하여 요청한 repository의 topic을 비교한 후, 알맞은 workflow를 찾는다<br>
&nbsp;&nbsp;3-1. 이때, 해당 repository에 등록된 topic을 참고한다.(즉, 사전에 topic 설정이 필요하다.)<br>
4. workflow를 찾으면 요청한 repository에 workflow를 commit(Create or Update)한다.<br>
5. commit된 workflow를 trigger 한다.<br>
6. 각 저장소에서 CI가 trigger되어 build가 시작된다.

## 설정 방법
actions의 목적은 plugin 개발자들이 workflowr 관리에 신경쓰지 않고 기존과 동일한 방법으로 배포할 수 있는 환경을 지향한다.<br>

### 1. 사전 설정
- 각 개발 repository는 topic을 설정해둔다.<br>
  - 해당 topic은 actions에 있는 workflow group와의 비교에 사용된다.
- github action secret에 PAT_TOKEN 등록<br>
  - public repository는 organization secret을 상속 받기때문에 별도의 설정은 필요없다.
  - private repository는 등록이 필요하다.

### 2. workflow 동기화 설정
관리하고자 하는 repository에 sync.yaml를 두면 자동으로 actions의 workflow와 동기화 된다.<br>
때문에, actions를 통해 workflow를 관리하고 싶다면, sync.yaml를 해당 repository에 두는 것으로 모든 준비는 끝난다.

### 3. 새로운 workflow 추가
추가하고 싶은 workflow 파일을 actions의 workflow group에 추가해둔다.<br>
이후 각 repository의 sync.yaml이 새롭게 추가된 workflow를 repository에 동기화해준다.<br>
새로운 group이 생긴다면, 해당 group과 workflow를 추가하기만 하면 된다.(물론 각 repository는 topic이 필요하다.)
```
├── README.md
├── backend             ★ workflow group
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

### 4. group과 일치하는 모든 저장소에 sync.yaml 배포
actions의 init_deploy CI를 실행하여 sync.yaml를 배포할 수 있다.<br>
init_deploy CI는 group을 input으로 받으며, 해당 group과 일치하는 topic을 가지고있는 모든 repository에 sync.yaml 배포된다.

이때 기존 workflow는 모두 삭제되니, 중요한 workflow는 backup해둔다.

## python script
python github client library를 이용해 구현되었다.<br>
manual로도 실행 가능하다.

`--init` 옵션을 통해 sync.yaml 파일을 지정한 단일 저장소에 commit할 수 있다.(actions를 clone하여 사용한다.)

```
usage: main.py [-h] --repo <owner/repo> [--init]

File push to github repository

optional arguments:
  -h, --help           show this help message and exit
  --repo <owner/repo>  Select specified repository.
  --init               Deploy sync workflow only.

Examples:
    python src/main.py --repo spaceone/inventory
    python src/main.py --repo spaceone/config --init
```
