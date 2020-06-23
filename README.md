# How to use

```
$ python src/app.py
```

### ENVIRONMENT = PRD

using `conf.yaml`

### ENVIRONMENT = DEV

using `dev-conf.yaml`

### Structure of the configuretaion file

```
# an example for conf.yaml

# Types of repositories
rTypes: 
  - name: backend
    # repositories which are included in a repository type
    repositories:
      - name: config
        url: github.com/spaceone-dev/config
      - name: identity
        url: github.com/spaceone-dev/identity
      ...
  - name: console
    repositories:
      - name: console
        url: github.com/spaceone-dev/console
```



## How to develop

### For development

* **Option 1. Push to dev**
  * push to `dev` branch. It detects the differences between the latest 2 commits. Then it uses `dev-conf.yaml` which includes repositories for test and development
* **Option 2. Merge `dev` into `master`**
  * Use **squash** because it refers to two latest commits. If not, it wouldn't be able to fetch two latest desired commits. (i.e - you might refer to multiple garbage commits in `dev` branch.)
* **Options 3. Just push to master**

