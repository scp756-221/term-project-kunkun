[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7037412&assignment_repo_type=AssignmentRepo)
# tprj
Term Project repo

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
