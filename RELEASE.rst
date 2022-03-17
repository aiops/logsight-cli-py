
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


Bash workflow
-------------

.. code-block:: console

    #. Update your local develop branch in case someone made changes to the remote develop branch
    git checkout develop
    git pull --rebase

    #. Created a new release id
    # Tags follow Semantic Versioning (https://semver.org): Major, Minor, Patch.

    prev_version=$(python setup.py --version)
    echo "Previous release: $prev_version"
    # update release version
    version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
    echo "New release: $version"

    # Create a branch from the current HEAD (does not touch local changes)
    git checkout -b release/$version develop

    # Warning: The following commands should be executed manually
    # Execute tests
    # $ python -m unittest discover tests`

    # Update the changelog
    # add commit message from HEAD to the previous tag
    # echo -e "$(git log --pretty='- %s' $prev_version..HEAD)\n\n$(cat CHANGELOG.rst)" > CHANGELOG.rst
    # Run gitchangelog to manually add changelog entries (the following command fails if it is the first release)
    gitchangelog ^$prev_version HEAD

    # Update automatically or manually the version in setup.py
    # $ vi setup.py or
    sed -i "/^version/s;[^ ]*$;'$version';" setup.py
    # BSD/MacOS: sed -i "" "/^version/s;[^ ]*$;'$version';" setup.py

    # Make the documentation
    # Documentation is at:
    # - https://www.sphinx-doc.org/en/master/tutorial/
    # - https://www.sphinx-doc.org/_/downloads/en/master/pdf/
    cd docs ; make clean ; make html ; cd ..

    # Warning: The following command should be executed manually
    # Execute tests
    # tox

    git commit -a -m "Preparation for release $version"

    #. Update main branch
    git checkout main
    git pull
    git merge --no-ff release/$version -m "Release $version"
    git tag -a $version -m "Release $version"
    git push --tags

    #. Update develop branch
    git checkout develop
    git pull
    git merge --no-ff release/$version -m "Release $version"
    # This step may well lead to a merge conflict (probably even, since we have changed the version number).
    # If so, fix it and commit.
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
