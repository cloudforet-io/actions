# actions
spaceone github action workflow repository

## 개요
spaceone의 repository가 사용하는 github action workflow의 repository이다.<br>
actions와 연동된 repository는 repository에서 최신 상태의 workflow를 가져온 후 CI를 수행할 수 있다.

actions는 github action의 workflows를 한곳에 모아서 관리하기 하는 것을 목적으로 하며,<br>
개발자들이 workflow 변경을 신경쓰지 않고 CI를 수행할 수 있는 환경을 제공한다.

<img src = "https://user-images.githubusercontent.com/19552819/148719878-f6b48702-65d2-49a0-88a7-ee3773d0305f.png" width="80%" height="80%">

## 설정 방법

### 1. 사전 설정
- 각 개발 repository의 topic을 설정해둔다.<br>
  - 해당 topic은 actions에 있는 workflow group와의 비교에 사용된다.
- github action secret에 PAT_TOKEN을 등록해둔다.<br>
  - workflow 요청 및 Build 수행에 사용된다.
    - public repository는 organization secret을 상속 받기때문에 별도의 설정은 필요없다.
    - private repository는 등록이 필요하다.

### 2. workflow 동기화 설정(sync.yaml 배포)
sync.yaml를 통해 각 repository는 최신 상태의 workflow를 actions로부터 가져올 수 있다.<br>
때문에 actions를 통해 workflow를 관리하고 싶다면, sync.yaml를 해당 repository에 두는 것으로 모든 준비는 끝난다.

#### 2-a. 처음 생성되는 repository에 sync.yaml 배포
수동 배포 혹은 [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)를 활용할 수 있다.

template repository의 경우, repository 생성 시 template repository의 내용을 바탕으로 repository를 생성한다.

#### 2-b. group과 일치하는 모든 기존 repository에 sync.yaml 배포
actions의 `[CI] init group`를 실행하여 sync.yaml를 배포할 수 있다.<br>
`[CI] init group`는 group을 input으로 받으며, 해당 group과 일치하는 topic을 가지고있는 모든 repository에 sync.yaml가 배포된다.

이때 기존 workflow는 모두 삭제되니, 중요한 workflow는 backup해둔다.<br>
**( `[CI] init group`는 각 repository의 모든 workflow를 삭제하기 때문에, Protection이 걸려있다. 관리자 승인이 없다면 실행되지 않는다.)**
<img src = "https://user-images.githubusercontent.com/19552819/148720016-58925e6d-692d-4223-a0ac-5037aba8650f.png" width="100%" height="100%">

#### 2-c. 단일 repository에 sync.yaml 배포
actions의 `[CI] init repository`를 실행하여 sync.yaml를 배포할 수 있다.<br>
`[CI] init repository`는 repository name을 input으로 받으며, 해당 repository에 sync.yaml가 배포된다.

이때 기존 workflow는 모두 삭제되니, 중요한 workflow는 backup해둔다.<br>
**(`[CI] init repository`는 repository의 모든 workflow를 삭제하기 때문에, Protection이 걸려있다. 관리자 승인이 없다면 실행되지 않는다.)**
<img src = "https://user-images.githubusercontent.com/19552819/148720070-5aecb426-cd3a-4579-9e54-6e20263254c2.png" width="100%" height="100%">

## 연동 후 사용법
- plugin
  - [README.md](https://github.com/spaceone-dev/actions/blob/master/plugin/workflows/README.md)

## 새로운 workflow 추가
추가하고 싶은 workflow 파일을 actions의 workflow group에 추가해둔다.<br>
이후 각 repository의 sync.yaml이 새롭게 추가된 workflow를 repository에 동기화해준다.<br>
새로운 group이 생긴다면, 해당 group과 workflow를 추가하기만 하면 된다.(물론 각 repository는 topic이 필요하다.)

```
.
├── README.md
├── backend
│   └── workflows           ★ 이곳 아래
├── common
│   └── workflows
│       ├── [Dispatch]sync_ci.yaml
│       └── [Push]sync_ci.yaml
├── plugin
│   └── workflows           ★ 이곳 아래
│       ├── README.md
│       ├── [Dispatch]release.yaml
│       └── [Push|dispatch]Build_dev.yaml
├── requirements.txt
└── src
    ├── main.py
    └── module
```