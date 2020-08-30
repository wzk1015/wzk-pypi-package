import os
import time
import json
import getpass
import warnings
import sys
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
        if key is None:
            return meta
        return meta[key]
    except FileNotFoundError:
        raise FileNotFoundError("Not a luna directory: " + str(path))


def _get_details(path, version):
    details = _read_meta(path, "version_details")
    key = "version " + version
    if key not in details.keys():
        raise ValueError("Unknown version: " + version)
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
                "cur_version"    : 0,
                "version_details": {},
                "history"        : []
            }
            json.dump(meta, f)
        _add_history(path, "luna init at " + path)
        print("init luna repo at " + path)


def commit(path, msg):
    version = str(int(_read_meta(path, "num_versions")) + 1)
    details = _read_meta(path, "version_details")
    os.mkdir(_luna(path, "versions", version))
    os.popen("cp -r {}/* {}".format(path, _luna(path, "versions", version))).close()
    details["version " + version] = {
        "creator": getpass.getuser(),
        "time"   : time.ctime(),
        "msg"    : msg,
    }
    _write_meta(path, num_versions=version, version_details=details, cur_version=version)
    _add_history(path, "luna commit version {} with message '{}'".format(version, msg))
    print("commit version " + version)


def revise(path, version, msg):
    version = str(version)
    details = _get_details(path, version)
    details["version " + version]["msg"] = msg
    _write_meta(path, version_details=details)
    _add_history(path, "luna revise version {} with message '{}'".format(version, msg))
    print("revise version " + version)


def reset(path, version):
    version = str(version)
    _get_details(path, version)
    os.popen("mv {} {}".format(_luna(path), os.path.join(path, "..", ".luna_temp"))).close()
    os.popen("rm -rf {}/*".format(path), "w").close()
    os.popen("mv {} {}".format(os.path.join(path, "..", ".luna_temp"), _luna(path))).close()
    os.popen("cp -r {} {}".format(_luna(path, "versions", version, "*"), path)).close()
    _write_meta(path, cur_version=version)
    _add_history(path, "luna reset to version " + version)
    print("reset to version " + version)


def log(path):
    pprint(_read_meta(path, "version_details"))


def history(path):
    pprint(_read_meta(path, "history"))


def info(path):
    pprint(_read_meta(path, None))


def view(path, version):
    version = str(version)
    pprint(_get_details(path, version)["version " + version])


def discard(path):
    os.popen("rm -rf {}".format(_luna(path))).close()
    print("discard luna repo at " + path)


def delete(path, version):
    if version == _read_meta(path, "cur_version"):
        _write_meta(path, cur_version="deleted")
    os.popen("rm -rf {}".format(_luna(path, "versions", version))).close()
    details = _get_details(path, version)
    details.pop("version " + version)
    _write_meta(path, version_details=details)
    print("delete version " + version)


def diff(path, v1, v2):
    raise NotImplementedError


def makefile(filepath, filename):
    os.popen("touch {}".format(os.path.join(filepath, filename))).close()


if __name__ == '__main__':
    p = os.getcwd()
    if len(sys.argv) < 2:
        raise ValueError("missing command arg")
    command = sys.argv[1]
    exec(command + "('" + p + "'," +
         ",".join(["'" + arg + "'" for arg in sys.argv[2:]])
         + ")")
