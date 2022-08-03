import subprocess
from pathlib import Path

REPO_DIR = Path("./repositories")

RCA_DIR = REPO_DIR / "rust-code-analysis"
RCA_CLI = "rust-code-analysis-cli"
RCA_URL = "https://github.com/mozilla/rust-code-analysis.git"

REPO_NAMES = [
    "FastCSV",
    "java-jwt",
    "jsoup",
    "Java-WebSocket"
]
REPO_URLS = [
    "https://github.com/osiegmar/FastCSV.git",
    "https://github.com/auth0/java-jwt.git",
    "https://github.com/jhy/jsoup.git",
    "https://github.com/TooTallNate/Java-WebSocket.git"
]
REPO_VERS = [
    ["v2.2.0", "v2.1.0"],
    ["4.0.0", "3.19.2"],
    ["jsoup-1.15.2", "jsoup-1.15.1"],
    ["v1.5.3", "v1.5.2"]
]

DATA_DIR = Path("./data")

def run_cmd(args, cwd):
    subprocess.run(args, check=True, cwd=cwd, stdout=subprocess.PIPE).stdout

def setup_rca():
    if RCA_DIR.is_dir():
        print("Updating rust-code-analysis...")
        run_cmd(["git", "checkout", "-f", "master"], RCA_DIR)
        run_cmd(["git", "pull"], RCA_DIR)
        run_cmd(["cargo", "build", "-p", RCA_CLI, "--release"], RCA_DIR)
        print("rust-code-analysis updated!")
    else:
        print("Cloning and building rust-code-analysis...")
        if not REPO_DIR.exists():
            REPO_DIR.mkdir(parents=True, exist_ok=True)
        run_cmd(["git", "clone", RCA_URL], REPO_DIR)
        run_cmd(["cargo", "build", "-p", RCA_CLI, "--release"], RCA_DIR)
        print("rust-code-analysis ready!")

def setup_repos():
    for index, repo_url in enumerate(REPO_URLS):
        repo_dir = REPO_DIR / REPO_NAMES[index]
        repo_name = REPO_NAMES[index]

        if repo_dir.is_dir():
            print("Updating " + repo_name + "...")
            run_cmd(["git", "checkout", "-f", "master"], repo_dir)
            run_cmd(["git", "pull"], repo_dir)
            print(repo_name + " updated!")
        else:
            print("Cloning " + repo_name + "...")
            run_cmd(["git", "clone", repo_url], REPO_DIR)
            print(repo_name + " cloned!")

def measure_repos():
    for index, repo_name in enumerate(REPO_NAMES):
        for repo_ver in REPO_VERS[index]:
            res_dir = DATA_DIR / repo_name / repo_ver

            print("Measuring " + repo_name + " " + repo_ver + "...")
            if not res_dir.exists():
                res_dir.mkdir(parents=True, exist_ok=True)
            run_cmd(["git", "checkout", repo_ver], REPO_DIR / repo_name)
            run_cmd(["cargo", "run", "-p", RCA_CLI, "--release", "--", "-m", "-p", Path("../" + repo_name), "-O", "json", "-o", "../.." / res_dir, "-l", "Java"], RCA_DIR)
            print(repo_name + " " + repo_ver + " measured!")

setup_rca()
setup_repos()
measure_repos()