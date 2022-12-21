import yaml
import os
import sys
from typing import List, Dict
from pathlib import Path
import datetime


def get_team_dirs(path: str) -> List[os.DirEntry[str]]:
    """
    path : need the trailing slash
    """
    dirs = os.scandir(path)
    result: list[os.DirEntry[str]] = []
    for dir in dirs:
        if dir.name.startswith('.') or not dir.is_dir(follow_symlinks=False):
            continue
        result.append(dir)
    return result


def get_sig_dirs() -> List[os.DirEntry[str]]:
    return get_team_dirs("sig/")


def get_corporation_dirs() -> List[os.DirEntry[str]]:
    return get_team_dirs("corporation/")


def get_now_date() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def get_all_metadata() -> Dict[str, Dict]:
    all_metadata: Dict[str, Dict] = {}
    for dir in get_sig_dirs():
        fname = dir.path + "/metadata.yml"
        if not Path(fname).exists():
            print("metadata no exists", dir.path)
            continue
        with open(fname, 'r', encoding="utf-8") as metadata_file:
            metadata = yaml.safe_load(metadata_file)
            name = metadata["name"]
            if "members" in metadata:
                metadata["_dir"] = dir.path
                if metadata["members"] == None:
                    metadata["members"] = []
                all_metadata[name] = metadata
    return all_metadata


def appendEvent(fname: str, new: list):
    obj = {"events": []}
    if Path(fname).exists():
        with open(fname, 'r', encoding="utf-8") as file:
            result = yaml.safe_load(file)
            obj["events"] = result["events"]
    obj["events"] += new
    with open(fname, 'w') as file:
        yaml.dump(obj, file, sort_keys=False)


def main():
    preHash = sys.argv[1]
    headHash = sys.argv[2]

    os.system("git reset --hard "+preHash)
    preMetadata = get_all_metadata()
    os.system("git reset --hard "+headHash)
    headMetadata = get_all_metadata()

    events: Dict[str, list] = {}
    for name in headMetadata:
        if name not in events:
            events[name] = []
        if name in preMetadata:
            headMembers = {
                member["id"]: member for member in headMetadata[name]["members"]}
            preMembers = {
                member["id"]: member for member in preMetadata[name]["members"]}
            joinMenbers = set(headMembers.keys()) - set(preMembers.keys())
            leaveMember = set(preMembers.keys()) - set(headMembers.keys())
            if len(joinMenbers) > 0:
                for id in joinMenbers:
                    events[name].append({
                        "type": "join",
                        "actor_id": headMembers[id]["id"],
                        "actor_handle": headMembers[id]["handle"],
                        "created_at": get_now_date(),
                    })
            if len(leaveMember) > 0:
                for id in leaveMember:
                    events[name].append({
                        "type": "leave",
                        "actor_id": preMembers[id]["id"],
                        "actor_handle": preMembers[id]["handle"],
                        "created_at": get_now_date(),
                    })
        else:
            for member in headMetadata[name]["members"]:
                events[name].append({
                    "type": "join",
                    "actor_id": member["id"],
                    "actor_handle": member["handle"],
                    "created_at": get_now_date(),
                })
    for name in events:
        if len(events[name]) == 0:
            continue
        appendEvent(headMetadata[name]["_dir"]+"/events.yaml", events[name])


if __name__ == "__main__":
    main()
