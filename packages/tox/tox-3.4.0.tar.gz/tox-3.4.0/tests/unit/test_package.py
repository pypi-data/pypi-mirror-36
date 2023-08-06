import re

import py
import pytest

from tox.config import parseconfig
from tox.package import get_build_info, get_package
from tox.session import Reporter, Session


def test_make_sdist(initproj):
    initproj(
        "example123-0.5",
        filedefs={
            "tests": {"test_hello.py": "def test_hello(): pass"},
            "tox.ini": """
        """,
        },
    )
    config = parseconfig([])
    session = Session(config)
    sdist = get_package(session)
    assert sdist.check()
    assert sdist.ext == ".zip"
    assert sdist == config.distdir.join(sdist.basename)
    sdist2 = get_package(session)
    assert sdist2 == sdist
    sdist.write("hello")
    assert sdist.stat().size < 10
    sdist_new = get_package(Session(config))
    assert sdist_new == sdist
    assert sdist_new.stat().size > 10


def test_make_sdist_distshare(tmpdir, initproj):
    distshare = tmpdir.join("distshare")
    initproj(
        "example123-0.6",
        filedefs={
            "tests": {"test_hello.py": "def test_hello(): pass"},
            "tox.ini": """
        [tox]
        distshare={}
        """.format(
                distshare
            ),
        },
    )
    config = parseconfig([])
    session = Session(config)
    sdist = get_package(session)
    assert sdist.check()
    assert sdist.ext == ".zip"
    assert sdist == config.distdir.join(sdist.basename)
    sdist_share = config.distshare.join(sdist.basename)
    assert sdist_share.check()
    assert sdist_share.read("rb") == sdist.read("rb"), (sdist_share, sdist)


def test_sdistonly(initproj, cmd):
    initproj(
        "example123",
        filedefs={
            "tox.ini": """
    """
        },
    )
    result = cmd("-v", "--sdistonly")
    assert not result.ret
    assert re.match(r".*sdist-make.*setup.py.*", result.out, re.DOTALL)
    assert "-mvirtualenv" not in result.out


def test_separate_sdist_no_sdistfile(cmd, initproj, tmpdir):
    distshare = tmpdir.join("distshare")
    initproj(
        ("pkg123-foo", "0.7"),
        filedefs={
            "tox.ini": """
            [tox]
            distshare={}
        """.format(
                distshare
            )
        },
    )
    result = cmd("--sdistonly")
    assert not result.ret
    distshare_files = distshare.listdir()
    assert len(distshare_files) == 1
    sdistfile = distshare_files[0]
    assert "pkg123-foo-0.7.zip" in str(sdistfile)


def test_separate_sdist(cmd, initproj, tmpdir):
    distshare = tmpdir.join("distshare")
    initproj(
        "pkg123-0.7",
        filedefs={
            "tox.ini": """
            [tox]
            distshare={}
            sdistsrc={{distshare}}/pkg123-0.7.zip
        """.format(
                distshare
            )
        },
    )
    result = cmd("--sdistonly")
    assert not result.ret
    sdistfiles = distshare.listdir()
    assert len(sdistfiles) == 1
    sdistfile = sdistfiles[0]
    result = cmd("-v", "--notest")
    assert not result.ret
    assert "python inst: {}".format(sdistfile) in result.out


def test_sdist_latest(tmpdir, newconfig):
    distshare = tmpdir.join("distshare")
    config = newconfig(
        [],
        """
            [tox]
            distshare={}
            sdistsrc={{distshare}}/pkg123-*
    """.format(
            distshare
        ),
    )
    p = distshare.ensure("pkg123-1.4.5.zip")
    distshare.ensure("pkg123-1.4.5a1.zip")
    session = Session(config)
    sdist_path = get_package(session)
    assert sdist_path == p


def test_installpkg(tmpdir, newconfig):
    p = tmpdir.ensure("pkg123-1.0.zip")
    config = newconfig(["--installpkg={}".format(p)], "")
    session = Session(config)
    sdist_path = get_package(session)
    assert sdist_path == p


def test_package_isolated_no_pyproject_toml(initproj, cmd):
    initproj(
        "package_no_toml-0.1",
        filedefs={
            "tox.ini": """
                [tox]
                isolated_build = true
            """
        },
    )
    result = cmd("--sdistonly")
    assert result.ret == 1
    assert result.outlines == ["ERROR: missing {}".format(py.path.local().join("pyproject.toml"))]


def toml_file_check(initproj, version, message, toml):
    initproj(
        "package_toml-{}".format(version),
        filedefs={
            "tox.ini": """
                        [tox]
                        isolated_build = true
                    """,
            "pyproject.toml": toml,
        },
    )
    reporter = Reporter(None)

    with pytest.raises(SystemExit, message=1):
        get_build_info(py.path.local(), reporter)
    toml_file = py.path.local().join("pyproject.toml")
    msg = "ERROR: {} inside {}".format(message, toml_file)
    assert reporter.reported_lines == [msg]


def test_package_isolated_toml_no_build_system(initproj, cmd):
    toml_file_check(initproj, 1, "build-system section missing", "")


def test_package_isolated_toml_no_requires(initproj, cmd):
    toml_file_check(
        initproj,
        2,
        "missing requires key at build-system section",
        """
    [build-system]
    """,
    )


def test_package_isolated_toml_no_backend(initproj, cmd):
    toml_file_check(
        initproj,
        3,
        "missing build-backend key at build-system section",
        """
    [build-system]
    requires = []
    """,
    )


def test_package_isolated_toml_bad_requires(initproj, cmd):
    toml_file_check(
        initproj,
        4,
        "requires key at build-system section must be a list of string",
        """
    [build-system]
    requires = ""
    build-backend = ""
    """,
    )


def test_package_isolated_toml_bad_backend(initproj, cmd):
    toml_file_check(
        initproj,
        5,
        "build-backend key at build-system section must be a string",
        """
    [build-system]
    requires = []
    build-backend = []
    """,
    )


def test_dist_exists_version_change(mock_venv, initproj, cmd):
    base = initproj(
        "package_toml-{}".format("0.1"),
        filedefs={
            "tox.ini": """
                [tox]
                isolated_build = true
                        """,
            "pyproject.toml": """
                [build-system]
                requires = ["setuptools >= 35.0.2"]
                build-backend = 'setuptools.build_meta'
                            """,
        },
    )
    result = cmd("-e", "py")
    assert result.ret == 0, result.out

    new_code = base.join("setup.py").read_text("utf-8").replace("0.1", "0.2")
    base.join("setup.py").write_text(new_code, "utf-8")

    result = cmd("-e", "py")
    assert result.ret == 0, result.out
