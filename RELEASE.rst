
Release workflow
================

Releases logsight CLI for Python to the following external systems:

+ GitHub_
+ `Test PyPI`_ and PyPI_

.. _github: https://github.com/aiops/logsight-cli-py
.. _test pypi: https://test.pypi.org/search/?q=%22logsight-cli-py%22&o=
.. _pypi: https://pypi.org/search/?q=%22logsight-cli-py%22&o=


Commit messages should be tagged to enable a detailed automated changelog generation:

+ 'chg' is for refactor, small improvement, cosmetic changes...
+ 'fix' is for bug fixes
+ 'new' is for new features, big improvement

Tags follow Semantic Versioning (https://semver.org): Major, Minor, Patch.


Bash workflow
-------------

.. code-block:: console

    #. Update your local develop branch in case someone made changes to the remote develop branch
    git checkout develop
    git pull --rebase

    # update release version
    prev_version=$(python setup.py --version)
    echo "Previous release: $prev_version"
    version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
    echo "New release:     version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
    echo "New release: $version""

    # Create a branch from the current HEAD (does not touch local changes)
    git checkout -b release/$version develop

    # Update automatically or manually the version in setup.py and ./logsight_cli/logsight-cli.py
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sed -i "/^VERSION/s;[^ ]*$;'$version';" setup.py ./logsight_cli/logsight_cli.py
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i "" "/^VERSION/s;[^ ]*$;'$version';" setup.py ./logsight_cli/logsight_cli.py
    else
        echo "OS is not supported"
    fi

    # Update the changelog
    gitchangelog ^$prev_version HEAD

    git commit -a -m "Preparation for release $version"

    #. Update main branch
    git checkout main
    git pull
    git merge --no-ff release/$version -m "Release $version"
    git tag -a $version -m "Release $version"
    git push --atomic --tags
    git push origin main

    #. Update develop branch
    git checkout develop
    git pull
    git merge --no-ff release/$version -m "Release $version"
    # Step may well lead to a merge conflict (since we changed version number). If so, fix it and commit.
    git push origin develop

    #. Remove release branch
    git branch -D release/$version

    # Warning: The following commands are implemented using Github actions
    # They should not be executed manually

    rm -rf build
    rm -rf dist
    python3 setup.py sdist bdist_wheel
    twine check dist/*

    twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-cli-py
    python3 -m pip uninstall logsight-cli-py

    twine upload dist/*
    python3 -m pip install logsight-cli-py
