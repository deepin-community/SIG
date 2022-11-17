from base64 import encode
import os, sys
from pathlib import Path
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any
import yaml
from utils import val_of_key


class SigInfo:
    id: str
    blog_url: str = ""
    homepage_url: str = ""
    display_name: dict[str, str] = {}
    package_repos: list[str] = []
    maintain_repos: list[str] = []
    proposal_issue_id: int = -1
    proposed_by_handle: str = ""
    proposed_by_display: str = ""
    created_date: date = datetime.date(datetime.now())

    def __init__(self, dir_path: str):
        path = Path(dir_path)
        self.id = path.name
        metadata_path = path / "metadata.yml"
        if metadata_path.exists():
            with open(dir_path + "/metadata.yml", 'r', encoding = 'utf-8') as file:
                metadata = yaml.safe_load(file)
                self.display_name['default'] = path.name if 'name' not in metadata else metadata['name']
                if 'blog' in metadata:
                    self.blog_url = metadata['blog']
                self.proposal_issue_id = val_of_key(metadata, ['proposal', 'issue'], -1)
                self.proposed_by_handle = val_of_key(metadata, ['proposal', 'by', 'handle'], "")
                self.proposed_by_display = val_of_key(metadata, ['proposal', 'by', 'display-name'], self.proposed_by_handle)
                if 'date-created' in metadata:
                    self.created_date = datetime.strptime(metadata['date-created'], '%Y/%m/%d').date()
        else:
            print("〇 SIG " + self.id + " doesn't have a metadata.yaml file provided")

    def name(self, locale: str) -> str:
        return self.display_name.get(locale, self.name.get('default', self.name.id))

    def blog_md(self) -> str:
        return " - " if not self.blog_url else "[博客]({0})".format(self.blog_url)

    def proposal_md(self) -> str:
        return " - " if self.proposal_issue_id <= 0 else "[申请PR](https://github.com/deepin-community/SIG/pull/{0})".format(self.proposal_issue_id)

    def proposer_md(self) -> str:
        return " - " if not self.proposed_by_handle else "[{1}](https://github.com/{0})".format(self.proposed_by_handle, self.proposed_by_display)
    
    def table_line(self, index: int) -> str:
        return "| {1} | [{0}]({0}/README.md) |{2}| [成员]({0}/MEMBERS.md) |{5}|{4}|{3}| - |\n".format(self.id, index, self.blog_md(), self.created_date.strftime("%Y/%m/%d"), self.proposer_md(), self.proposal_md())


def get_sig_dirs() -> list[os.DirEntry[str]]:
    path = "sig/"
    dirs = os.scandir( path )
    result : list[os.DirEntry[str]] = []
    for dir in dirs:
        if dir.name.startswith('.') or not dir.is_dir(follow_symlinks = False):
            continue
        result.append(dir)
    return result


def get_missing_sigs(existing_sig_dirs: list[os.DirEntry[str]]) -> tuple[list[str], list[str]]:
    existing : list[str] = []
    missing : list[str] = []
    with open("sig/LISTS.md", 'r', encoding = 'utf-8') as file:
        content = file.read()
        for dir in existing_sig_dirs:
            if content.find('[' + dir.name + ']') == -1:
                missing.append(dir.name)
            else:
                existing.append(dir.name)
    return (missing, existing)


def main():
    if sys.version_info < (3, 10):
        print("Need python >= 3.10 to run.")
        exit(1)

    if len(sys.argv) < 2:
        print("Need argument:")
        print("    --check-need-update")
        print("    --update-sig-list")
        exit(1)
    
    match sys.argv[1]:
        case "--test":
            a = SigInfo("./sig/dde-porting")
            print(a.table_line(1))

        case "--check-need-update":
            dirs = get_sig_dirs()
            (missing, existing) = get_missing_sigs(dirs)
            for e in existing:
                print("√ " + e + " FOUND in LISTS.md!")
            for m in missing:
                print("× " + m + " NOT FOUND in LISTS.md!")
            if len(missing) > 0:
                exit(2)

        case "--update-sig-list":
            dirs = get_sig_dirs()
            (missing, _) = get_missing_sigs(dirs)
            if len(missing) == 0:
                print("Don't need to update anything, peacefully exiting :)")
                exit(0)
            lines : list[str] = []
            with open("sig/LISTS.md", 'r', encoding = 'utf-8') as file:
                lines = file.readlines()
                # remove last empty line
                if not lines[-1]:
                    lines = lines[:-1]
                # append missing SIGs
                for m in missing:
                    print("Generating information for: {0}".format(m))
                    sig_info = SigInfo("./sig/{0}".format(m))
                    lines.append(sig_info.table_line(len(lines) - 1))
            with open("sig/LISTS.md", 'w', encoding = 'utf-8') as file:
                file.writelines(lines)

    print("Done.")


if __name__ == "__main__":
    main()
