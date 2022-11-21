import argparse
import os
import sys
from pathlib import Path
import subprocess
import yaml
import json
from typing import Any
from utils import val_of_key


def create_repo(org: str, reponame: str, templaterepo_org_n_name: str = ""):
    args = ['gh', 'repo',
            'create', "{0}/{1}".format(org, reponame),
            '--public']
    if not templaterepo_org_n_name:
        args += ['--template', templaterepo_org_n_name]
    
    subprocess.run(args)


def call_gh_api(method: str, path: str, raw_fields: list[str] = [], dryrun: bool = False) -> int:
    '''
    raw_fields: ["field1='val'", "field2='val'"]
    '''
    args = ['gh', 'api', 
            '--method', method,
            '-H', 'Accept: application/vnd.github+json',
            path]
    for raw_field in raw_fields:
        args += ['-f', raw_field]
    
    if dryrun == True:
        print(args)
        return 0
    else:
        proc = subprocess.run(args)
        return proc.returncode


def require_file_arg(parser: argparse.ArgumentParser):
    parser.add_argument('-f', '--file',
                        action='store',
                        help='the GitHub Team configuration YAML file',
                        required=True)


def require_slug_arg(parser: argparse.ArgumentParser):
    parser.add_argument('-s', '--slug',
                        action='store',
                        help='the GitHub Team slug',
                        required=True)


def require_ref_cur_arg(parser: argparse.ArgumentParser):
    parser.add_argument('-r', '--ref',
                        action='store',
                        help='the json file used as a reference file',
                        required=True)
    parser.add_argument('-c', '--cur',
                        action='store',
                        help='the json file used as the current state',
                        required=True)


def action_validate_handle(parser: argparse.ArgumentParser):
    '''
    The YAML file passed MUST be an array just contain user data.
    The file WILL be modified if the handle is incorrect.
    '''
    pass


def create_team(org: str, slug: str, dryrun: bool):
    call_gh_api("POST", "/orgs/{0}/teams".format(org), [
        "name='{0}'".format(slug),
        "privacy='closed'"
    ], dryrun=dryrun)


def action_ensure_team_exists(parser: argparse.ArgumentParser):
    '''
    team-management.py --action ensure_team_exists --file metadata.yml
    '''
    require_file_arg(parser)
    args = parser.parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        print("Missing input files")
        exit(61)
    with open(file_path, 'r', encoding = 'utf-8') as file:
        metadata = yaml.safe_load(file)
        team_slug = val_of_key(metadata, ['team'], '')
        if not team_slug:
            print("missing team slug")
            exit(61)
        ret = call_gh_api("GET", "/orgs/{0}/teams/{1}".format(args.organization, team_slug))
        if ret != 0:
            create_team(args.organization, team_slug, args.dry_run)



def action_team_repo_management(parser: argparse.ArgumentParser):
    '''
    team-management.py --action team_repo_management --ref ref.json --cur cur.json --permission push --slug team-slug
    '''
    require_ref_cur_arg(parser)
    require_slug_arg(parser)
    parser.add_argument('-p', '--permission',
                        action='store',
                        choices=['push', 'maintain'],
                        help='the repo permission',
                        required=True)
    args = parser.parse_args()
    reffile_path = Path(args.ref)
    curfile_path = Path(args.cur)
    if not reffile_path.exists() or not curfile_path.exists():
        print("Missing input files")
        exit(61)

    with open(reffile_path, 'r', encoding = 'utf-8') as reffile:
        with open(curfile_path, 'r', encoding = 'utf-8') as curfile:
            cur_repos = json.load(curfile)
            ref_repos = json.load(reffile)
            need_removal = [item for item in cur_repos if item not in ref_repos]
            need_addition = [item for item in ref_repos if item not in cur_repos]
            for ghrepo in need_addition:
                # TODO: check repo exist, create if not exist
                call_gh_api('PUT', '/orgs/{0}/teams/{1}/repos/{0}/{2}'.format(args.organization, args.slug, ghrepo),
                            ["permission='{0}'".format(args.permission)], dryrun=args.dry_run)
                pass
            for ghrepo in need_removal:
                call_gh_api('DELETE', '/orgs/{0}/teams/{1}/repos/{0}/{2}'.format(args.organization, args.slug, ghrepo),
                            dryrun=args.dry_run)


def action_team_member_management(parser: argparse.ArgumentParser):
    '''
    team-management.py --action team_member_management --ref ref.json --cur cur.json --slug team-slug
    '''
    require_ref_cur_arg(parser)
    require_slug_arg(parser)
    args = parser.parse_args()
    reffile_path = Path(args.ref)
    curfile_path = Path(args.cur)
    if not reffile_path.exists() or not curfile_path.exists():
        print("Missing input files")
        exit(61)

    with open(reffile_path, 'r', encoding = 'utf-8') as reffile:
        with open(curfile_path, 'r', encoding = 'utf-8') as curfile:
            cur_accounts = json.load(curfile)
            ref_accounts = json.load(reffile)
            need_removal = [item for item in cur_accounts if item not in ref_accounts]
            need_addition = [item for item in ref_accounts if item not in cur_accounts]
            for ghaccount in need_addition:
                call_gh_api('PUT', '/orgs/{0}/teams/{1}/memberships/{2}'.format(args.organization, args.slug, ghaccount['handle']),
                            ["role='member'"], dryrun=args.dry_run)
            for ghaccount in need_removal:
                call_gh_api('DELETE', '/orgs/{0}/teams/{1}/memberships/{2}'.format(args.organization, args.slug, ghaccount['handle']),
                            ["role='member'"], dryrun=args.dry_run)


def main():
    if sys.version_info < (3, 10):
        print("Need python >= 3.10 to run.")
        exit(1)
    parser = argparse.ArgumentParser(
                    prog = 'Team Management Helper',
                    description = 'Provide the ability to manage GitHub Team',
                    epilog = 'Please also look at the Justfile which calls this file!')
    parser.add_argument('-a', '--action',
                        action='store',
                        help='the action type that is going to preform',
                        required=True)
    parser.add_argument('-o', '--organization',
                        action='store',
                        help='the GitHub organization related to this operation',
                        default='deepin-community')
    parser.add_argument('-d', '--dry-run',
                        action='store_true',
                        help='turn on dry-run for debugging')
    [args, _] = parser.parse_known_args()

    if args.dry_run:
        print("!!! Be aware, the action MIGHT or MIGHT NOT support dry-run !!!")
        print("!!!/-- DRY-RUN-OPTION-ENABLED --\\!!!\n")

    funname = "action_{0}".format(args.action)
    if (funname not in globals()):
        print("Action not supported")
        exit(61)
    globals()[funname](parser)

    if args.dry_run:
        print("\n!!!\\-- DRY-RUN-OPTION-ENABLED --/!!!")


if __name__ == "__main__":
    main()