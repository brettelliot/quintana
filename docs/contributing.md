# Contributing

## Making changes to the juniper project
We use a simple git rebase workflow from [here](http://reinh.com/blog/2009/03/02/a-git-workflow-for-agile-teams.html)

```sh
# 1. Pull to update your local master
git checkout master
git pull origin master

# 2. Check out a feature branch
git checkout -b be-feature

# 2. Or switch to it if it already exists
git checkout be-feature

# 3. Do work in your feature branch, committing early and often
git add .
git add -p
git commit -m "my changes"
git push

# 4. Rebase frequently to incorporate upstream changes
# Get stuff from origin master, then apply my changes on top with rebase
git fetch origin master
git rebase origin/master

# 5. Interactive rebase (squash) your commits
git rebase -i origin/master

# 6. Merge your changes with master
git checkout master
git merge be-feature

# 7. Push your changes to the upstream
git push origin master

# 8a. optional: tag important things, such as releases
git tag 1.0.0

# 8b. push single tag
git push origin 2.0.0

# 8c. Push all tags
git push origin --tags

# 9a. Go back to your feature branch and do more work
git checkout be-feature

# 9b. Replay your changes on top of your feature branch
git pull
```

## Remove a docker volume
Sometimes you just want to clean up everything (like the postgres db). To remove a docker volume (like delete the postgres db) first shutdown the container and volumes. Then find and delete a specific volume and remove it:

```sh
docker-compose down --volumes
docker volume ls
docker volume rm <name_of_volume>
```
