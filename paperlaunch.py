#! /usr/bin/env python3
import git

from os.path import abspath, join, curdir, pardir

script_dir = abspath(join(__file__, pardir))
conf_dir = script_dir
template_dir = abspath(join(script_dir, 'templates'))

# Read conf globally
# Get a token from https://github.com/settings/tokens
from configparser import ConfigParser
conf = ConfigParser()
with open(join(conf_dir, 'settings.conf'), 'r') as f:
    conf.read_file(f)

# Set up a new LaTeX paper project


def paperlaunch(name='paperlaunch-project', github=False, public=False):
    """
    Generate a LaTeX project for scientific publication

    Args:
        name (str): Project/repo name
        github (bool): Create a repository online with token/settings from conf
        private (bool): Make online repository private
    """

    private = not public

    if github:
        local_repo, remote_repo = create_repo_github(name, private=private)

    else:
        local_repo = create_repo_local(name)

    copy_tex_files(name)
    git_index = local_repo.index
    git_index.add(['paper.tex', 'si.tex', 'README.md', 'Makefile',
                   'bibliography.bib'])
    git_index.commit("Initial setup from templates")


def copy_tex_files(name, **kwargs):
    from string import Template
    from shutil import copyfile
    from os import chdir

    chdir(name)

    mapping = conf['template'].items()
    mapping = {k.upper(): v for k, v in mapping}

    if 'TITLE' not in mapping:
        mapping['TITLE'] = name

    for target in ("paper.tex", "si.tex", "README.md"):
        with open(join(template_dir, target)) as f:
            source = Template(f.read())
            text = source.safe_substitute(mapping)
        with open(target, 'w') as f:
            f.write(text)

    for target in ("Makefile", "bibliography.bib"):
        copyfile(join(template_dir, target), target)


def create_repo_local(name):
    local_repo = git.Repo.init(path=join(curdir, name), mkdir=True)
    return local_repo


def create_repo_github(name, private=True):
    """Create named repo on github, clone to local and return interfaces

    Args:
        name (str): Project/repo name
        private (bool): Make online repository private

    Returns:
        (local_repo (git.Repo), remote_repo (github.Repository)
    """
    # Github repo
    from github import Github
    token = conf['github']['token']

    gh = Github(login_or_token=token)

    org = conf.get('github', 'org', fallback=None)
    if org is None:
        actor = gh.get_user()
    else:
        org = gh.get_organization('SMTG-UCL')
        actor = org
    remote_repo = actor.create_repo(
        name,
        description="Description",
        gitignore_template="TeX",
        private=private)

    # Clone to local for setup
    local_repo = git.Repo.clone_from(remote_repo.clone_url, join(curdir, name))

    return (local_repo, remote_repo)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Set up a new LaTeX project directory")

    parser.add_argument(
        'name',
        type=str,
        help="Project name. Used as folder name "
        "and repo address.")
    parser.add_argument(
        '--public',
        action='store_true',
        help="Don't make the repository private")
    parser.add_argument(
        '--github',
        '--gh',
        action='store_true',
        help="Make a repository on Github")
    args = parser.parse_args()

    paperlaunch(**vars(args))


if __name__ == '__main__':
    main()
