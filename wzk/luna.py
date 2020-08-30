import os
import time
import json
import getpass
import warnings
import sys
from pprint import pprint
from difflib import Differ
import filecmp


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


def reset(path, version=None):
    if version is None:
        version = _read_meta(path, "cur_version")
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


def _diff_compare(in_lines1, in_lines2):
    l1 = in_lines1.split("\n")
    l2 = in_lines2.split("\n")
    d = Differ()
    result = list(d.compare(l1, l2))
    result = "\n".join(result)
    return result


def diff(path, version1=None, version2=None):
    def _replace(string):
        return string.replace(_luna(path), '').replace('/versions/', 'version') \
            .replace(r'\versions\ '[:-1], 'version')

    def _diff_recur(d: filecmp.dircmp, key, v1path, v2path):
        for file in d.__getattr__(key):
            path1 = os.path.join(v1path, file)
            path2 = os.path.join(v2path, file)
            lines1, lines2 = "", ""
            if key != "right_only":
                with open(path1, errors="ignore") as f1:
                    lines1 = f1.read()
            if key != "left_only":
                with open(path2, errors="ignore") as f2:
                    lines2 = f2.read()
            if key == "diff_files":
                print("diff file {} {}".format(_replace(path1), _replace(path2)))
            else:
                print("unique file {}".format(_replace(path1) if key == "left_only"
                                              else _replace(path2)))
            print(_diff_compare(lines1, lines2))
        for name, sd in d.subdirs.items():
            _diff_recur(sd, key, os.path.join(v1path, name),
                        os.path.join(v2path, name))
    
    v1 = _read_meta(path, "cur_version") if version1 is None else str(version1)
    v2 = "[not staged]" if version2 is None else str(version2)
    dir1 = _luna(path, "versions", v1)
    dir2 = _luna(path, "versions", v2) if version2 is not None else path
    d = filecmp.dircmp(dir1, dir2, hide=[os.curdir, os.pardir, ".luna"], ignore=['.git', '.DS_Store'])
    print("Overall diff".center(50, "-"))
    d.report_full_closure()
    print("Different files".center(50, "-"))
    _diff_recur(d, "diff_files", dir1, dir2)
    print("Unique files".center(50, "-"))
    print(("Version " + v1 + " only").center(50, "-"))
    _diff_recur(d, "left_only", dir1, dir2)
    print(("Version " + v2 + " only").center(50, "-"))
    _diff_recur(d, "right_only", dir1, dir2)


def makefile(filepath, filename):
    os.popen("touch {}".format(os.path.join(filepath, filename))).close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("missing command arg")
    exec("{}({},{})".format(sys.argv[1], os.getcwd(),
                            ",".join(["'" + arg + "'" for arg in sys.argv[2:]])))
