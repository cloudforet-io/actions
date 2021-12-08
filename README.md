# actions
중앙 집중형 github action workflow 관리 도구

## 개요
spaceone MSA에 공통적으로 사용되는 github action workflow를 관리하고, 각 repository에 배포한다.<br>
배포된 workflow는 각 repository에서 Trigger될 때 action의 deploy workflow를 호출하여 지속적으로 최신 상태를 유지할 수 있다.

<img src = "https://user-images.githubusercontent.com/19552819/145136525-608930c0-8ea4-44d0-a5db-a127a495fee1.png" width="50%" height="50%">


## 사용 방법
github action을 trigger하여 배포할 수 있다.
- input
  - [required]group : 동일한 workflow를 사용하는 group을 지정.
  - [option]repository : 특정 repository만을 지정하고 싶을때 사용.
![스크린샷 2021-12-08 오전 11 20 35](https://user-images.githubusercontent.com/19552819/145137059-251ecb7a-6279-471f-bb85-298c9ccf580e.png)

### group에 대해
spaceone-dev의 repository는 동일한 github action workflow를 사용하는 경우가 있다.<br>
때문에 이러한 동일한 workflow를 사용하는 Repository를 group으로 묶고 deploy시에 이것을 활용한다.

|group|repository|
|---|---|
|backend|spaceone-dev/inventory,identity,config,notification....|
|plugin|spaceone-dev/plugin-aws...,plugin-google....,plugin-azure....   |
|console|spaceone-dev/console|
|console-api|spaceone-dev/console-api|

## 설정

### 배포 대상 repository 설정
conf.yaml에 정의한다.<br>
새로운 repository가 추가되거나, 관리 대상에서 벗어난 repository가 있다면, 이곳에서 추가/삭제를 하면된다.<br>

```
rTypes:                            
  backend:                        # workflow group
    - name: spaceone-dev/config   # repository name
    - name: spaceone-dev/identity
  console:
    - name: spaceone-dev/console
  plugin:
    - name: spaceone-dev/plugin-azure-cloud-service-inven-collector
```


### workflow 추가
각 group의 workflows에 추가하고 싶은 workflow 파일을 추가해둔다.<br>
추후 deploy workflow가 동작하면서, 새롭게 추가된 파일을 지정 repository에 추가해준다.
```
├── README.md
├── backend
│   └── workflows     ★ 이곳
│       └── sample.yaml
├── console
│   └── workflows     ★ 이곳
│       └── sample.yaml
├── plugin
│   └── workflows     ★ 이곳
│       └── sample.yaml  
├── conf.yaml
├── requirements.txt
├── src
│   ├── main.py
│   └── module
└── venv
    ├── bin
    ├── lib
    └── pyvenv.cfg
```

### 새로운 group 추가
새로운 group이 추가된다면, group 이름의 directory를 생성 후 workflows/<..>.yaml을 생성한다.<br>
[update중...]
