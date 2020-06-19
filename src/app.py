import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
import gitFunctions as git

CONF_LOCATION="conf.yaml"
CLONE_PATH="temp"
COPY_SRC=None # To be determined by repository
COPY_DEST="/".join([CLONE_PATH,".github", "workflows"])
GIT_ADD_PATH = COPY_DEST[len(CLONE_PATH)+1:]
repositoryTypes=git.getRepositoryTypes(CONF_LOCATION)
newCommit, oldCommit = git.getCommits()
repositoryTypeNamesToPush=git.getRepositoryNamesToPush(repositoryTypes, newCommit, oldCommit)

repositoriesToPush = git.filterReposToPush(repositoryTypes, repositoryTypeNamesToPush)

for repo in repositoriesToPush:
    COPY_SRC = "/".join([repo["rTypeName"], "workflows"])

    repoObj=git.cloneRepository(repo["name"], repo["url"], CLONE_PATH)
    git.copyData(COPY_SRC, COPY_DEST)
    git.push(repoObj, repo["url"], GIT_ADD_PATH)
    git.removeData(CLONE_PATH)