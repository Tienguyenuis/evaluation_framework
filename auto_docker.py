import subprocess
from make_scripts import maketrainlp, maketrainnc, makeevallp, makeevalnc

def make_container_train():
    subprocess.run(["docker", "stop", "graph_embedding"])
    subprocess.run(["docker", "rm", "graph_embedding"])
    subprocess.run(["docker", "run", "-d", "-P", "-it", "--privileged=true", "--name", "graph_embedding", "-v", "/home/congttn/badne:/data", "graph_embedding:0.5", "/bin/bash"])


def make_container_evaluate():
        subprocess.run(["docker", "stop", "graph_embedding_eval"])
        subprocess.run(["docker", "rm", "graph_embedding_eval"])
        subprocess.run(["docker", "run", "-d", "-P", "-it", "--privileged=true", "--name", "graph_embedding_eval", "-v", "/home/congttn/badne:/data", "graph_embedding_eval:0.5", "/bin/bash"])
def install_requirements(method):
    try:
        requirements = "pip install -r /data/code/methods/" + method + "/requirements.txt"
        subprocess.run(["docker", "exec", "-i", "graph_embedding", "/bin/bash", "-c", requirements])
    except:
        pass

    try:
        requirements3 = "pip3 install -r /data/code/methods/" + method + "/requirements.txt"
        subprocess.run(["docker", "exec", "-i", "graph_embedding", "/bin/bash", "-c", requirements3])
    except:
        pass
    try:
        installation = "./data/code/methods/" + method + "/installation.sh"
        subprocess.run(["docker", "exec", "-i", "graph_embedding", "/bin/bash", "-c", installation])
    except:
        pass

def execute_train():
    try:
        subprocess.run(["docker", "exec", "-i", "graph_embedding", "/bin/bash", "-c", "./data/web/instructions/trainlp.sh"])
    except:
        pass
    try:
        subprocess.run(["docker", "exec", "-i", "graph_embedding", "/bin/bash", "-c", "./data/web/instructions/trainnc.sh"])
    except:
        pass
def execute_evaluation():
    try:
        subprocess.run(["docker", "exec", "-i", "graph_embedding_eval", "/bin/bash", "-c", "./data/web/instructions/evaluatelp1.sh"])
        subprocess.run(["docker", "exec", "-i", "graph_embedding_eval", "/bin/bash", "-c", "./data/web/instructions/evaluatelp2.sh"])
    except:
        pass

    try:
        subprocess.run(["docker", "exec", "-i", "graph_embedding_eval", "/bin/bash", "-c", "./data/web/instructions/evaluatenc1.sh"])
        subprocess.run(["docker", "exec", "-i", "graph_embedding_eval", "/bin/bash", "-c", "./data/web/instructions/evaluatenc2.sh"])
    except:
        pass
