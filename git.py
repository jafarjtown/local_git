import os
import sys
import zipfile
import json


BASE_DIR = os.path.expanduser("~/minimal_git/")
REPOS_DIR = os.path.expanduser(os.path.expanduser("~/minimal_git/repos/"))



# BASE_DIR = "./minimal/"
# REPOS_DIR = BASE_DIR + "repos/"
db = {}

if not os.path.isdir(os.path.normpath(REPOS_DIR)):
    os.makedirs(os.path.normpath(REPOS_DIR))
    
if os.path.isfile(os.path.normpath(os.path.expanduser(BASE_DIR + "git.db"))):
    db = json.load(open(os.path.normpath(os.path.expanduser(BASE_DIR + "git.db"))))
    
    
def dump():
    try:
       json.dump(db, open(os.path.normpath(os.path.expanduser(BASE_DIR + "git.db")), "w"), indent=4)
    except Exception as e:
        print("Database cant be saved", e)
    
    
def create_repository(name: str):
    
    if name not in db:
        db[name] = []
        os.makedirs(os.path.normpath(REPOS_DIR + name))
    else:
        print(f"Repository {name} already exists")
    dump()
    
    
def list_repositories():
    if len(db) > 0:
        for rep in db.keys():
            print(rep)
    else:
        print("Theres no repositories")
        
        
        
def list_commits(repo):
    if repo in db:
        print("\n".join(db[repo]))
    else:
        print(f"No such repository {repo}")
        

def zipdir(path, repo, commit):
    
    gitignore = []
    if os.path.isfile(f"{path}gitignore"):
        with open(f"{path}gitignore") as ignore:
            gitginore = [i.strip() for i in ignore.readlines()]
    
    with zipfile.ZipFile(
        os.path.normpath(REPOS_DIR + repo + f"/{commit}.zip"),
        "w",
        zipfile.ZIP_DEFLATED
    ) as ziph:
        for root, dirs, files in os.walk(path):
            for _file in files:
                if _file not in gitignore:
                    ziph.write(os.path.join(root, _file))
                    
                    
def commit(repo, name ):
    if repo in db:
        commits = db[repo]
        if name not in commits:
            zipdir('.', repo, name )
            commits.append(name)
            db[repo] = commits
            dump()
        else:
            print(f"Commit with {name} already exists.")
    else:
        print(f"the repository {repo} does not exists.")
        
        
def clone(repo, commit):
    if repo in db:
        if commit in db[repo]:
            path = os.path.normpath(REPOS_DIR + repo + f"{commit}.zip")
            try:
                with zipfile.ZipFile(
                    path, "r"
                ) as ziph:
                    ziph.extractall(path=os.curdir)
            except Exception as e:
                print("Cloning failed", e)
        else:
            print(f"no such commit {commit} in {repo}")
    else:
        print("No such repository")
        
        
        
        
if __name__ == "__main__":
    repo = ""
    commit_ = ""
    if len(sys.argv) > 1:
        if sys.argv[1] == "clone" and len(sys.argv) == 4:
            repo = sys.argv[2]
            commit_ = sys.argv[3]
             
            print(f"Cloning {commit_} from {repo}")
            clone(repo, commit_ )
        elif sys.argv[1] == "commit" and len(sys.argv) == 4:
            repo = sys.argv[2]
            commit_ = sys.argv[3]
             
            print(f"commiting current directory {commit_} into {repo}")
            commit(repo, commit_ )
        elif sys.argv[1] == "list" and len(sys.argv) == 2:
            list_repositories()
        elif sys.argv[1] == "list" and len(sys.argv) == 3:
            repo = sys.argv[2]
            print(f"Listing commit from {repo}")
            list_commits(repo)
        elif sys.argv[1] == "create" and len(sys.argv) == 3:
            repo = sys.argv[2]
            
            print(f"Creating Repositiory {repo}")
            create_repository(repo)
        else:
            print("""
                Unknown commabd, try:
                clone <repo> <commit>
                commit <repo> <commit>
                list
                list <repo>
                create <repo>
            
            """)