import subprocess
from pathlib import Path

DATA_DIR = Path("./data")
REPO_DIR = Path("./repositories")
RCA_DIR = REPO_DIR / "rust-code-analysis"
RCA_CLI = "rust-code-analysis-cli"
RCA_URL = "https://github.com/mozilla/rust-code-analysis.git"

REPO_NAMES = [
    "FastCSV",
    "java-jwt",
    "Java-WebSocket",
    "gson",
    "spring-kafka",
    "mockito"
]
REPO_URLS = [
    "https://github.com/osiegmar/FastCSV.git",
    "https://github.com/auth0/java-jwt.git",
    "https://github.com/TooTallNate/Java-WebSocket.git",
    "https://github.com/google/gson.git",
    "https://github.com/spring-projects/spring-kafka.git",
    "https://github.com/mockito/mockito.git"
]
REPO_VERS = [
    ["v2.2.0"],
    ["3.16.0", "3.17.0", "3.18.0", "3.18.1", "3.18.2", "3.18.3", "3.19.0", "3.19.1", "3.19.2", "4.0.0"],
    ["v1.5.3"],
    ["gson-parent-2.8.2", "gson-parent-2.8.3", "gson-parent-2.8.4", "gson-parent-2.8.5", "gson-parent-2.8.6", "gson-parent-2.8.7", "gson-parent-2.8.8", "gson-parent-2.8.9", "gson-parent-2.9.0", "gson-parent-2.9.1"],
    ["v2.8.0", "v2.8.1", "v2.8.2", "v2.8.3", "v2.8.4", "v2.8.5", "v2.8.6", "v2.8.7", "v2.8.8", "v2.9.0"],
    ["v4.1.0", "v4.2.0", "v4.3.0", "v4.3.1", "v4.4.0", "v4.5.0", "v4.5.1", "v4.6.0", "v4.6.1", "v4.7.0"]
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
            if index == 4 or index == 5:
                run_cmd(["git", "checkout", "-f", "main"], repo_dir)
            else:
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