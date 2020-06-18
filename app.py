from git import Repo
import os
import yaml
import shutil
import requests
def git_push(repo ):
    try:
        repo.git.add(update=True)
        repo.index.commit("COMMIT_MESSAGE")
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code') 
# repo.git.add(update=True)

def getRepositoryTypes(configurationFile="conf.yaml"):
    with open(configurationFile) as y:
        rTypes=yaml.load(y)["rTypes"]
    return rTypes
def getCommits(gitPath="."):
    repo = Repo(gitPath) # using current directory .git
    new, old = repo.iter_commits(max_count=2)

    return new, old
def getRepositoryNamesToPush(rTypes, new, old):
    rTypeNames=set([rType["name"] for rType in rTypes])
    rTypesToPullRequest = set()

    for diff in old.diff(new):
        # print(diff)
        _rTypeNameA = diff.a_path.split("/")[0]
        _rTypeNameB = diff.b_path.split("/")[0]
        # A or B path has the path
        if _rTypeNameA in rTypeNames:
            print("[Repoisotry Type]", _rTypeNameA, "Changed")
            print("changed file : ", diff.a_path)
            print()
            rTypesToPullRequest.add(_rTypeNameA)
        else:
            pass

        if _rTypeNameB in rTypeNames:
            print("[Repoisotry Type]", _rTypeNameB, "Changed")
            print("changed file : ", diff.b_path)
            print()
            rTypesToPullRequest.add(_rTypeNameB)
        else:
            pass
    return rTypesToPullRequest
    # rTypeToPullRequest = set([rType["name"] for rType in rTypes])
    
def pullRequest(rTypes, rTypeNames):
    CLONE_PATH="temp"
    # rTypeNames is a Set. This should not be duplicated
    for rTypeName in list(rTypeNames):
        rType=None
        for _rType in rTypes:
            if _rType["name"] == rTypeName:
                rType=_rType
                break
        
        repositories = rType["repositories"]
        
        for repository in repositories:
            # clone and push changes
            try:
                shutil.rmtree(CLONE_PATH)
                print("deleted CLONE_PATH")
            except Exception as e:
                print( e)
                print("Failed to delete CLONE_PATH")
                print("This wouldn't matter")
            
            _repository = Repo.clone_from("https://"+repository["url"], CLONE_PATH, branch='master')
            shutil.rmtree("/".join([CLONE_PATH, ".github", "workflows"]))
            shutil.copytree(rTypeName, "/".join([CLONE_PATH, ".github", "workflows"]))
            _repository.git.add("/".join([".github", "workflows"]), update=True)
            _repository.index.commit("JINSU BOT")
            origin = _repository.remote(name='origin')
            if os.environ.get("ENVIRONMENT") == "PRD":
                origin.push()
            else:
                print("You don't push. Push only when the ENVIRONMENT is PRD")
            shutil.rmtree(CLONE_PATH)

repositoryTypes=getRepositoryTypes()
print("===")
print("RepositoryTypes")
print(repositoryTypes)

newCommit, oldCommit = getCommits()
print("===")
print("Commits")
print("New", newCommit)
print("Old", oldCommit)

repositoryTypeNamesToPush=getRepositoryNamesToPush(repositoryTypes, newCommit, oldCommit)
print("===")
print("RepositoryTypeNamesToPush")
print(repositoryTypeNamesToPush)

pullRequest(repositoryTypes, repositoryTypeNamesToPush)