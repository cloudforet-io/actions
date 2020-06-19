from git import Repo
import os
import yaml
import shutil
import logging

def getRepositoryTypes(configurationFile):
    logging.info("Configuration File : %s", configurationFile)
    with open(configurationFile) as y:
        rTypes = yaml.safe_load(y)["rTypes"]
    logging.info("Read rTypes from %s. rTypes : %s", configurationFile, str(rTypes))
    return rTypes


def getCommits(gitPath="."):
    repo = Repo(gitPath)  # using current directory .git
    new, old = repo.iter_commits(max_count=2)
    logging.info("New commit - %s", str(new))
    logging.info("Old commit - %s", str(old))
    return new, old


def getRepositoryNamesToPush(rTypes, new, old):
    # only repository type names
    rTypeNames = set([rType["name"] for rType in rTypes])
    rTypeNamesToPullRequest = set()

    for diff in old.diff(new):
        # print(diff)
        _rTypeNameA = diff.a_path.split("/")[0]
        _rTypeNameB = diff.b_path.split("/")[0]
        # A or B path has the path
        if _rTypeNameA in rTypeNames:
            logging.info("[Repoisotry Type] %s Changed.", _rTypeNameA)
            logging.info("changed file : %s", diff.a_path)
            rTypeNamesToPullRequest.add(_rTypeNameA)
        else:
            pass

        if _rTypeNameB in rTypeNames:
            logging.info("[Repoisotry Type] %s Changed", _rTypeNameB)
            logging.info("changed file : %s", diff.b_path)
            rTypeNamesToPullRequest.add(_rTypeNameB)
        else:
            pass
    return rTypeNamesToPullRequest


def filterReposToPush(rTypes, rTypeNames):
    CLONE_PATH = "temp"
    # rTypeNames is a Set. This should not be duplicated
    for rTypeName in list(rTypeNames):
        rType = None
        for _rType in rTypes:
            if _rType["name"] == rTypeName:
                rType = _rType
                break
        logging.info("Start a pull request job for repository-%s", rType["name"])
        repositories = rType["repositories"]
        for repo in repositories:
            repo["rTypeName"] = rTypeName
    return repositories


def cloneRepository(repositoryName, repositoryUrl, clonePath):
    clonePath = "temp"
    try:
        shutil.rmtree(clonePath)
        logging.info("Deleted CLONE_PATH. %s", clonePath)
    except Exception as e:
        print(e)
        print("Failed to delete CLONE_PATH")
        print("This wouldn't matter")
    try:
        _repository = Repo.clone_from("https://" + repositoryUrl, clonePath, branch='master')
        logging.info("Cloned from %s", repositoryUrl)
        return _repository
    except Exception as e:
        logging.warning("Already exists files or dirs. %s", clonePath)


def copyData(copySrc, copyDest):
    try:
        shutil.rmtree(copyDest)
        logging.info("Deleted copyDest ahead. " + copyDest)
    except Exception as e:
        logging.warning("Skip deleting copyDest ahead. %s", copyDest)
    shutil.copytree(copySrc, copyDest)
    logging.info("Copied file %s => %s", copySrc, copyDest)
    # for repository in repositories:
    # clone and push changes

def push(repository, url, gitAddPath):
    logging.info("Git add path : %s", gitAddPath)
    repository.git.add(gitAddPath)
    repository.index.commit("[BOT] New github action has been published.")

    origin = repository.remote(name='origin')

    origin.set_url(
        "https://" + os.environ.get("GIT_USERNAME") + ":" + os.environ.get("GIT_PASSWORD") + "@" + url)
    if os.environ.get("ENVIRONMENT") == "PRD":
        origin.push()
        logging.info("Successfully pushed to " + repository["name"])
    else:
        logging.info("You don't push because your ENVIRONMENT is not PRD")

def removeData(path):
    shutil.rmtree(path)