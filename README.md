[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7037412&assignment_repo_type=AssignmentRepo)
# CMPT 756 Project -- Team Kunkun

### File Structure


Directory/file | 1st Sub Dir/file | 2nd Sub Dir/file| Note
---- | ----- | ----- | ----- 
.github/ | workflow/ | ci-system-v1.1.yml | CI test command
ci/ | v1.1/ | compose.yaml | Set up an integration test of S3.
ci/ | v1.1/ | conftest.py | Add S3 comment_address, comment_port and comment_url.
ci/ | v1.1/ | create_tables.py | Create comment tables for CI test.
ci/ | v1.1/ | Dockerfile | Add command to run CI test for S3 and add parameters for S3.
ci/ | v1.1/ | flake-dirs.txt | Add directory path for S3.
ci/ | v1.1/ | user.py | Python  API for the user service.
ci/ | v1.1/ | test_user.py | CI test script for user service.
ci/ | v1.1/ | comment.py | Python  API for the comment service.
ci/ | v1.1/ | test_comment.py | CI test script for comment service.
ci/ | create-local-tables.sh | - | Create comment  table in local DynamoDB
cluster/ | - | - | Modify config files to support tests.
gatling | simulations/proj756/ | ReadTables.scala | Add ReadTables.scala for s3
gatling | test/ | - | Add gatling tests for comments which simulate 100, 500 and 1000 users access comment service
loader/ | app.py | - | Add loader for comments.csv
mcli/ | mcli.py | - | Client interaction with s1, s2, s3 and add a new monitor to the new service s3.
s3/ | v1/ and v2/ | app.py | The Comment service.
s3/ | v1/ and v2/ | Dockerfile | Command and port to run service.
s3/ | v1/ and v2/ | requirement.txt | The versions of packages that service needs.
eks-tpl.mak | - | - | Update the cluster configuration.
k8s-tpl.mak | - | - |Add circuit breaker for s3

---

### 1. Instantiate the template files
Copy the file `cluster/tpl-vars-blank.txt` to `cluster/tpl-vars.txt`
and fill in all the required values in `tpl-vars.txt`.  These include
things like your AWS keys, your GitHub signon, and other identifying
information. 
~~~
$ tools/shell.sh
~~~
~~~
$ make -f k8s-tpl.mak templates
~~~
### 2. Start cluster
~~~
make -f eks.mak start
~~~

### 3. Ensure AWS DynamoDB is initialized
~~~
$ aws dynamodb list-tables
~~~
The resulting output should include tables `User`, `Music` and `Comment`.

### 4.Provision the cluster
Create a namespace c756ns and set it as the default 
~~~
$ kubectl create ns c756ns
$ kubectl config set-context --current --namespace=c756ns
~~~
Deploy all services
~~~
make -f k8s.mak provision
~~~

### 5. Grafana and Kiali

1. Print the Grafana URL and Kiali URL
~~~
make -f k8s.mak grafana-url
~~~
~~~
make -f k8s.mak kiali-url
~~~
2. Start a new terminal window, send initial loads to the system. Change the number `10` to `100`, `500`, `1000` and observe the changes in grafana
~~~
./gatling-10-music.sh
~~~
~~~
./gatling-10-comment.sh
~~~
~~~
./gatling-10-user.sh
~~~
3. Stop gatling
~~~
tools/kill-gatling.sh
~~~
4. Close cluster
~~~
make -f eks.mak stop
~~~

----




## Git workflow
All the group members in Kunkun need to follow this git workflow.

### Cloning and forking the repository
 <code>git clone <i>clone-url</i></code>

### Add features 
Before you make any changes, you should make a branch. Remember to **never
commit to master**. The command `git status` will tell you what branch you are
on. 
1. **Update master.** Before you make any changes, first checkout master

   ```
   git checkout master
   ```

   and pull in the latest changes

   ```
   git pull
   ```

   This will make it so that your changes are against the very latest master,
   which will reduce the likelihood of merge conflicts due to your changes
   conflicting with changes made by someone else.
2. **Create a branch.** Once you have done this, create a new branch. We need two main branches, one is develop, and the other is master, only develop can merge to master. 
    To create the branch, run

   <code>
   git checkout -b <i>branch-name</i>
   </code>
3. **Make your changes and commit them.** Once you have created your branch,
   make your changes and commit them. Remember to keep your commits atomic and  write helpful commit messages.
    <pre><code>git add <i>filename [filename ...]</i>
   git commit
   </code></pre>

4. **Push up your changes.** Do this by running

   <pre><code>
   git checkout develop  
   git merge --no-ff <i>branch-name</i>  
   git branch -d <i>branch-name</i>  
   git push origin develop. 

   </code></pre>
