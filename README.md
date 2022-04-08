[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7037412&assignment_repo_type=AssignmentRepo)
# CMPT 756 Project -- Team Kunkun

Directory/file | Note
---- | ----- 
s1/ | the User service

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


### Reference

This is the tree of this repo. 


The CI material at `ci` and `.github/workflows` are presently designed for Assignment 7 and the course's operation. They're not useable for you and should be removed. If you are ambitious or familiar with GitHub action, the one flow that may be _illustrative_ is `ci-to-dockerhub.yaml`. **It is not directly useable as you team repo will not use templates.**
```
├── ./.github
│   └── ./.github/workflows
│       ├── ./.github/workflows/ci-a1.yaml
│       ├── ./.github/workflows/ci-a2.yaml
│       ├── ./.github/workflows/ci-a3.yaml
│       ├── ./.github/workflows/ci-mk-test.yaml
│       ├── ./.github/workflows/ci-system-v1.1.yaml
│       ├── ./.github/workflows/ci-system-v1.yaml
│       └── ./.github/workflows/ci-to-dockerhub.yaml
├── ./ci
│   ├── ./ci/v1
│   └── ./ci/v1.1
```

Be careful to only commit files without any secrets (AWS keys). 
```
├── ./cluster
```

These are templates for the course and should be removed.
```
├── ./allclouds-tpl.mak
├── ./api-tpl.mak
├── ./az-tpl.mak
│   ├── ./ci/create-local-tables-tpl.sh
│   │   ├── ./ci/v1/compose-tpl.yaml
│       ├── ./ci/v1.1/compose-tpl.yaml
│   ├── ./cluster/awscred-tpl.yaml
│   ├── ./cluster/cloudformationdynamodb-tpl.json
│   ├── ./cluster/db-nohealth-tpl.yaml
│   ├── ./cluster/db-tpl.yaml
│   ├── ./cluster/dynamodb-service-entry-tpl.yaml
│   ├── ./cluster/loader-tpl.yaml
│   ├── ./cluster/s1-nohealth-tpl.yaml
│   ├── ./cluster/s1-tpl.yaml
│   ├── ./cluster/s2-dpl-v1-tpl.yaml
│   ├── ./cluster/s2-dpl-v2-tpl.yaml
│   ├── ./cluster/s2-nohealth-tpl.yaml
│   ├── ./cluster/tpl-vars-blank.txt
│   ├── ./db/app-tpl.py
├── ./eks-tpl.mak
│   ├── ./gcloud/gcloud-build-tpl.sh
│   └── ./gcloud/shell-tpl.sh
├── ./gcp-tpl.mak
├── ./k8s-tpl.mak
├── ./mk-tpl.mak
│   │   ├── ./s2/standalone/README-tpl.md
│   │   └── ./s2/standalone/unique_code-tpl.py
│   │   └── ./s2/v1/unique_code-tpl.py
```

Support material for using this repo in the CSIL lab.
```
├── ./csil-build
```

The core of the microservices. `s2/v1.1`, `s2/v2`, and `s2/standalone`  are for use with Assignments. For your term project, work and/or derive from the `v1` version.
```
├── ./db
├── ./s1
├── ./s2
│   ├── ./s2/standalone
│   │   ├── ./s2/standalone/__pycache__
│   │   └── ./s2/standalone/odd
│   ├── ./s2/test
│   ├── ./s2/v1
│   ├── ./s2/v1.1
│   └── ./s2/v2
```

`results` and `target` need to be created but they are ephemeral and do not need to be saved/committed.
```
├── ./gatling
│   ├── ./gatling/resources
│   ├── ./gatling/results
│   │   ├── ./gatling/results/readmusicsim-20220204210034251
│   │   └── ./gatling/results/readusersim-20220311171600548
│   ├── ./gatling/simulations
│   │   └── ./gatling/simulations/proj756
│   └── ./gatling/target
│       └── ./gatling/target/test-classes
│           ├── ./gatling/target/test-classes/computerdatabase
│           └── ./gatling/target/test-classes/proj756
```

Support material for using this repo with GCP (GKE).
```
├── ./gcloud
```

A small job for loading DynamoDB with some fixtures.
```
├── ./loader
```

Logs files are saved here to reduce clutter.
```
├── ./logs
```

Assignment 4's CLI for the Music service. It's non-core to the Music microservices. At present, it is only useable for the Intel architecture. If you are working from an M1 Mac, you will not be able to build/use this. The workaround is to build/run from an (Intel) EC2 instance.
```
├── ./mcli
```

Deprecated material for operating the API via Postman.
```
├── ./postman
```

Redundant copies of the AWS macros for the tool container. You should use the copy at [https://github.com/overcoil/c756-quickies](https://github.com/overcoil/c756-quickies) instead.
```
├── ./profiles
```

Reference material for istio and Prometheus.
```
├── ./reference
```

Assorted scripts that you can pick and choose from:
```
└── ./tools
```

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
