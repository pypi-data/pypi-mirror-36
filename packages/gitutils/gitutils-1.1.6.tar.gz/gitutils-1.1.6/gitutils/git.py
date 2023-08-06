import logging
from pathlib import Path
from sys import stderr
import subprocess
from time import sleep
from typing import Sequence, List, Tuple, Optional
from operator import attrgetter
import collections
try:
    import colorama
    MAGENTA = colorama.Back.MAGENTA
    BLACK = colorama.Back.BLACK
    colorama.init()
except ImportError:
    MAGENTA = BLACK = ''

"""
replaced by git status --porcelain:
  ['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
  ['git','--no-pager','diff','HEAD'], # check for uncommitted work

DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches
"""


def findbranch(ok: str, rdir: Path) -> List[Tuple[Path, str]]:
    """find all branches in tree not matching ok"""

    rdir = Path(rdir).expanduser()

    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']

    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    branch = []
    for d in dlist:
        try:
            ret = subprocess.check_output(cmd, cwd=d,
                                          universal_newlines=True).rstrip()

            if ok not in ret:
                branch.append((d, ret))
        except subprocess.CalledProcessError as e:
            print(d, e)

    return branch


def gitemail(path: Path, user: str,
             exclude: Sequence[str]=None) -> Optional[List[Tuple[str, int]]]:
    """
    returns email addresses of everyone who ever made a Git commit in this repo.
    """
    path = Path(path).expanduser().resolve()

    if baddir(path):
        raise FileNotFoundError(f'no Git repos found under {path}')

    cmd = ['git', 'log', '--pretty="%ce"']

    ret = subprocess.check_output(cmd, cwd=path, universal_newlines=True)
    ret = ret.replace('"', '')
    ret = filter(None, ret.split('\n'))  # remove blanks

    # rset = set(ret)
    # emails = list(rset.difference(set(exclude))) if exclude else list(rset)

    emails = collections.Counter(ret).most_common()
# %% output
    print(MAGENTA + path.stem + BLACK)

    for email in emails:
        print(email[0], email[1])

    return emails


def baddir(path: Path) -> bool:
    path = path.expanduser()

    return (path / '.nogit').is_file() or not (path / '.git').is_dir()


def fetchpull(mode: str, rdir: Path) -> List[str]:
    """
    handles recursive "git pull" and "git fetch"

    Reference:
    ----------
    format mini-language:
    https://docs.python.org/3/library/string.html#format-specification-mini-language
    """
    # leave .resolve() for useful error messages
    rdir = Path(rdir).expanduser().resolve()

    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    Lmax = len(max(map(attrgetter('name'), dlist), key=len))
    print('git', mode, len(dlist), 'paths under', rdir)

    failed = []
    for d in dlist:

        print(f' --> {d.name:<{Lmax}}', end="", flush=True)
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            subprocess.check_output(['git'] + mode.split(), cwd=d,
                                    universal_newlines=True)
            print(end="\r")
        except subprocess.CalledProcessError:
            failed.append(d.name)

        sleep(.1)  # don't hammer the remote server

    print()
    if failed:
        logging.error(f'git {mode} {rdir}')
        # no backslash allowed in f-strings
        print('\n'.join(failed), file=stderr)

    return failed


def gitpushall(rdir: Path, verbose: bool=False) -> List[Path]:
    rdir = Path(rdir).expanduser()
    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    dir_topush = []
    for d in dlist:
        if detectchange(d, verbose):
            dir_topush.append(d)

    return dir_topush


def listchanged(path: Path) -> List[str]:
    """very quick check"""
    ret = subprocess.check_output(['git', 'ls-files', '--modified'],
                                  universal_newlines=True,
                                  cwd=path)

    ret = ret.split('\n')

    return ret


def detectchange(d: Path, verbose: bool=False) -> bool:
    """in depth check"""
    c1 = ['git', 'status', '--porcelain']  # uncommitted or changed files

    try:
        # %% detect uncommitted changes
        ret = subprocess.check_output(c1, cwd=d, universal_newlines=True)
        changed = _print_change(ret, d, verbose)
        if changed:
            return changed

# %% detect committed, but not pushed
        c0 = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
        branch = subprocess.check_output(c0, cwd=d, universal_newlines=True)[:-1]

        c2 = ['git', 'diff', '--stat', f'origin/{branch}..']
        ret = subprocess.check_output(c2, cwd=d, universal_newlines=True)
        changed = _print_change(ret, d, verbose)
    except subprocess.CalledProcessError as e:
        logging.error(f'{d} {e.output}')

    return changed


def _print_change(ret: str, d: Path, verbose: bool=False) -> bool:
    changed = False

    if ret:
        changed = True
        if verbose:
            print(MAGENTA + str(d))
            print(BLACK + ret)

    return changed
