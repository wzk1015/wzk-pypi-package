import os
import time
import json
import getpass
import warnings
from pprint import pprint


def _luna(path, *args):
    ans = os.path.join(path, ".luna", *args)
    return ans


def _write_meta(path, **kwargs):
    try:
        with open(_luna(path, "metadata.json"), "r") as f:
            meta = json.load(f)
        for k, v in kwargs.items():
            meta[k] = v
        with open(_luna(path, "metadata.json"), "w") as f:
            json.dump(meta, f)
    except FileNotFoundError:
        raise FileNotFoundError("Not a luna directory: " + str(path))


def _read_meta(path, key):
    try:
        with open(_luna(path, "metadata.json"), "r") as f:
            meta = json.load(f)
            return meta[key]
    except FileNotFoundError:
        raise FileNotFoundError("Not a luna directory: " + str(path))


def _get_details(path, version):
    details = _read_meta(path, "version_details")
    key = "version " + str(version)
    if key not in details.keys():
        raise ValueError("Unknown version: " + str(version))
    return details


def _add_history(path, info):
    h = _read_meta(path, "history")
    h.append({
        "user": getpass.getuser(),
        "time": time.ctime(),
        "info": info,
    })
    _write_meta(path, history=h)


def init(path):
    try:
        _read_meta(path, "create_time")
        warnings.warn("Already a luna repo: " + str(path))
        return
    except FileNotFoundError:
        os.mkdir(_luna(path))
        os.mkdir(_luna(path, "versions"))
        with open(_luna(path, "metadata.json"), "w") as f:
            meta = {
                "create_time"    : time.ctime(),
                "creator"        : getpass.getuser(),
                "path"           : path,
                "num_versions"   : 0,
                "version_details": {},
                "history"        : []
            }
            json.dump(meta, f)
        _add_history(path, "luna init at " + path)


def commit(path, msg):
    version = _read_meta(path, "num_versions") + 1
    details = _read_meta(path, "version_details")
    os.mkdir(_luna(path, "versions", str(version)))
    os.popen("cp -r {}/* {}".format(path, _luna(path, "versions", str(version)))).close()
    details["version " + str(version)] = {
        "creator": getpass.getuser(),
        "time"   : time.ctime(),
        "msg"    : msg,
    }
    _write_meta(path, num_versions=version, version_details=details)
    _add_history(path, "luna commit version " + str(version))


def log(path):
    pprint(_read_meta(path, "version_details"))


def history(path):
    pprint(_read_meta(path, "history"))


def view(path, version):
    pprint(_get_details(path, version)["version " + str(version)])


def revise(path, version, msg):
    details = _get_details(path, version)
    details["version " + str(version)]["msg"] = msg
    _write_meta(path, version_details=details)
    _add_history(path, "luna revise version " + str(version) +
                 " with message '" + msg + "'")


def reset(path, version):
    _get_details(path, version)
    os.popen("mv {} {}".format(_luna(path), os.path.join(path, "..", ".luna_temp"))).close()
    delete = os.popen("rm -rf {}/*".format(path), "w")
    delete.write("y")
    delete.close()
    os.popen("mv {} {}".format(os.path.join(path, "..", ".luna_temp"), _luna(path))).close()
    os.popen("cp -r {} {}".format(_luna(path, "versions", str(version), "*"), path)).close()
    _add_history(path, "luna reset to version " + str(version))


def remove(path):
    os.popen("rm -rf {}".format(_luna(path))).close()


def diff():
    raise NotImplementedError


def makefile(filepath, filename):
    os.popen("touch {}".format(os.path.join(filepath, filename))).close()


if __name__ == '__main__':
    p = "/Users/wzk/Desktop/"
    init(p)
    makefile(p, "1")
    commit(p, "commit 1")
    makefile(p, "2")
    commit(p, "commit 2")
    revise(p, 2, "commit 3 new message")
    reset(p, 1)
    reset(p, 2)
    history(p)
    #commit(p, "third commit!")
    #init(p)