from base64 import encode
import os, sys

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
                    lines.append("| {1} | [{0}]({0}/README.md) | [博客](https://deepin-community.github.io/{0}/) | [成员]({0}/MEMBERS.md) | [申请PR](#) | - | - | - |\n".format(m, len(lines) - 1))
            with open("sig/LISTS.md", 'w', encoding = 'utf-8') as file:
                file.writelines(lines)

    print("Done.")


if __name__ == "__main__":
    main()
