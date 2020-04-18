# Contributing

## Making changes to the juniper project
We use a simple git rebase workflow from [here](http://reinh.com/blog/2009/03/02/a-git-workflow-for-agile-teams.html)

```sh
# 1. Pull to update your local master
git checkout master
git pull origin master

# 2. Check out a feature branch
git checkout -b be-feature

# 3. Do work in your feature branch, committing early and often
git add -p
git commit -m "my changes"

# 4. Rebase frequently to incorporate upstream changes
git fetch origin master
git rebase origin/master

# 5. Interactive rebase (squash) your commits
git rebase -i origin/master

# 6. Merge your changes with master
git checkout master
git merge be-feature

# 7. Push your changes to the upstream
git push origin master
```

## How this was made
Balsam was added as a submodule using:

```sh
git submodule add -b juniper https://github.com/brettelliot/balsam balsam
```


