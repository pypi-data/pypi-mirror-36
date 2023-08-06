import prmt
from headlines import h3
from buildlib import git


def commit_msg(
    margin: tuple = (0, 1),
    editor: bool = True,
) -> str:

    return prmt.string(
        question='Enter COMMIT message:\n',
        margin=margin,
        force_val=True,
        editor=editor,
    )


def branch(margin: tuple = (1, 1)) -> str:

    default = git.cmd.get_default_branch().val

    return prmt.string(
        question='Enter BRANCH name:\n', default=default, margin=margin
    )


def confirm_status(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    print(h3('Git Status'))
    git.cmd.status()

    return prmt.confirm(
        question='GIT STATUS ok?\n', default=default, margin=margin
    )


def confirm_diff(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    print(h3('Git Diff'))
    git.cmd.diff()

    return prmt.confirm(
        question='GIT DIFF ok?\n',
        default=default,
        margin=margin,
    )


def should_run_git(
    default: str = 'y',
    margin: tuple = (1, 0),
) -> bool:

    return prmt.confirm(
        question='Run ANY GIT COMMANDS?\n',
        default=default,
        margin=margin,
    )


def should_add_all(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    return prmt.confirm(
        question='Run GIT ADD ALL ("git add --all")?\n',
        default=default,
        margin=margin
    )


def should_commit(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    return prmt.confirm(
        question='Run GIT COMMIT?\n', default=default, margin=margin
    )


def should_tag(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    return prmt.confirm(
        question='Run GIT TAG?\n', default=default, margin=margin
    )


def should_push(
    default: str = 'y',
    margin: tuple = (1, 1),
) -> bool:

    return prmt.confirm(
        question='GIT PUSH to GITHUB?\n', default=default, margin=margin
    )
