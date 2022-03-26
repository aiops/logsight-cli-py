Release workflow
================

Releases logsight CLI for Python to the following external systems:

-   [GitHub](https://github.com/aiops/logsight-cli-py)
-   [Test PyPI](https://test.pypi.org/search/?q=%22logsight-cli-py%22&o=) and
    [PyPI](https://pypi.org/search/?q=%22logsight-cli-py%22&o=)

Commit messages should be tagged to enable a detailed automated
changelog generation:

-   \'chg\' is for refactor, small improvement, cosmetic changes\...
-   \'fix\' is for bug fixes
-   \'new\' is for new features, big improvement

Tags follow Semantic Versioning (<https://semver.org>): Major, Minor,
Patch.

Bash workflow
-------------

```bash

function merge_successful {
    echo "Status of git merge: $1"
    if [ $1 -ne 0 ]; then
        echo "The merge failed. Manually fix the code, and commit."
        exit 1  
    fi
} 

#. Update your local develop branch in case someone made changes to the remote develop branch
git checkout develop
git pull --rebase

# update release version
prev_version=$(python setup.py --version)
echo "Previous release: $prev_version"
version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
echo "New release: $version"

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
merge_successful($?)

git tag -a $version -m "Release $version"
git push --atomic --tags
git push origin main

#. Update develop branch
git checkout develop
git pull
git merge --no-ff release/$version -m "Release $version"
merge_successful($?)
git push origin develop

#. Remove release branch
git branch -D release/$version

# Warning: The following commands are implemented using Github actions
# They should not be executed manually
exit(0)

rm -rf build
rm -rf dist
python3 setup.py sdist bdist_wheel
twine check dist/*

twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-cli-py
python3 -m pip uninstall logsight-cli-py

twine upload dist/*
python3 -m pip install logsight-cli-py
```
