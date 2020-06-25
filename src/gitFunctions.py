from git import Repo
import os, subprocess
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


def getRepositoryTypeNamesToPush(rTypes, new, old):
    # only repository type names
    rTypeNames = set([rType["name"] for rType in rTypes])
    rTypeNamesToPush = set()

    for diff in old.diff(new):
        logging.info(diff)
        _rTypeNameA = diff.a_path.split("/")[0]
        _rTypeNameB = diff.b_path.split("/")[0]
        # A or B path has the path
        if _rTypeNameA in rTypeNames:
            logging.info("[Repoisotry Type] %s Changed.", _rTypeNameA)
            logging.info("changed file : %s", diff.a_path)
            rTypeNamesToPush.add(_rTypeNameA)
        else:
            pass

        if _rTypeNameB in rTypeNames:
            logging.info("[Repoisotry Type] %s Changed", _rTypeNameB)
            logging.info("changed file : %s", diff.b_path)
            rTypeNamesToPush.add(_rTypeNameB)
        else:
            pass
    logging.info("[Repository Types] to push - %s", str(rTypeNamesToPush))
    return rTypeNamesToPush

def getAllRepositories(rTypes):
    repositories = []
    for rType in rTypes:
        repositories.append(rType["repositories"])
    return repositories
def filterReposToPush(rTypes, rTypeNames):
    repositories = []
    # rTypeNames is a Set. This should not be duplicated
    for rTypeName in list(rTypeNames):
        rType = None
        for _rType in rTypes:
            if _rType["name"] == rTypeName:
                rType = _rType
                break
        _repositories = rType["repositories"]
        for _repo in _repositories:
            _repo["rTypeName"] = rTypeName
            repositories.append(_repo)
    logging.info("[Repository] filtered repos to push - %s", str(repositories))
    return repositories


def cloneRepository(repositoryName, repositoryUrl, clonePath):
    try:
        shutil.rmtree(clonePath)
        logging.info("Deleted CLONE_PATH. %s", clonePath)
    except Exception as e:
        logging.info(e)
        logging.info("Failed to delete CLONE_PATH")
        logging.info("This wouldn't matter")
    try:
        _author_username = os.environ.get("AUTHOR_USERNAME", "ACTION_BOT")
        _author_email = os.environ.get("AUTHOR_EMAIL", "NO_EMAIL")
        _config_path = "/".join([clonePath, ".git", "config"])
        logging.info("Author - %s/%s", _author_username, _author_email)

        _repository = Repo.clone_from("https://" + repositoryUrl, clonePath, branch='master')
        logging.info("Cloned from %s", repositoryUrl)
        subprocess.call(["git", "config", "-f", _config_path, "user.name", _author_username])
        subprocess.call(["git", "config", "-f", _config_path, "user.email", _author_email])

        return _repository
    except Exception as e:
        logging.warning("Already exists files or dirs. %s", clonePath)
        _repository = Repo(clonePath)
        return _repository



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
    origin.push()
    logging.info("[SUCCESS] Pushed to " + url)

def removeData(path):
    shutil.rmtree(path)