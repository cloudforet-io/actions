import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
import gitFunctions as git




# initialize variables
CONFIGURATION_PATH=os.environ.get("CONFIGURATION_PATH", "NO_CONFIGURE")
if(CONFIGURATION_PATH=="NO_CONFIGURE"):
    logging.error("No configuration file. Use CONFIGURATION_PATH based on project root.")
    exit(1)
CLONE_PATH="temp"
COPY_SRC=None # To be determined by repository
COPY_DEST="/".join([CLONE_PATH,".github", "workflows"])
GIT_ADD_PATH = COPY_DEST[len(CLONE_PATH)+1:]

# start functions
repositoryTypes=git.getRepositoryTypes(CONFIGURATION_PATH)
newCommit, oldCommit = git.getCommits()
repositoryTypeNamesToPush=git.getRepositoryTypeNamesToPush(repositoryTypes, newCommit, oldCommit)

repositoriesToPush = git.filterReposToPush(repositoryTypes, repositoryTypeNamesToPush)

for repo in repositoriesToPush:
    COPY_SRC = "/".join([repo["rTypeName"], "workflows"])
    logging.info(repo)
    repoObj=git.cloneRepository(repo["name"], repo["url"], CLONE_PATH)
    git.copyData(COPY_SRC, COPY_DEST)
    git.push(repoObj, repo["url"], GIT_ADD_PATH)
    git.removeData(CLONE_PATH)