from .pkg_tracker import RequirementsUpdater


def main(work_branches=['master'], base='master'):
    RequirementsUpdater(work_branches, base).create_pull()

if __name__ == "__main__":
    main()