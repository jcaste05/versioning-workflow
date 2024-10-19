# versioning-workflow
In this repository, automatic versioning is implemented through the use of conventional commits and npm standard-version. Also, the use of GitHub actions is exemplified to verify code writing standards and the use of unit tests with pytest.

## Overview

- Automated testing with **Pytest**.
- Automated format test for python scripts with **flake8**.
- Automated versioning with [conventinal commits](https://www.conventionalcommits.org/en/v1.0.0/), [npm standard-version](https://www.npmjs.com/package/standard-version) and **Git tags**.
- Automated release creation based on execution of tests and bumping version.

## Prerequisites

- **Google Colab** in order to use a console with Node.js and npm without installing it.

## How the Repository Was Created

### 1. Initial Repository Setup
1. **Create repository**:
   - Add a default .gitignore for Node proyect to avoid adding _node_modules_ to the repository later.
   - Create a Personal Access Token if you don´t have it.

2. **Clone repository on GoogleColab**:
     ```bash
     !git clone https://github.com/<<user_name>>/versioning-workflow.git
     !git config --global user.name <<user_name>>
     !git config --global user.email <<user_email>>
     %cd versioning-workflow/
     ```
3. **Create Node.js project and install npm standard-version**:
    - Create Node.js. This must have created package.json with the current version 1.0.0 of te project, the scripts that we can run with npm and the dependencies.
      ```bash
      !npm init -y
      ```
   - Install standard-version at "devDependencies" (--save-dev). This must have created package-lock.json with specific dependencies and _node_modules_ with the packages. This folder will not be uploaded to the repo because of the .gitignore. Only is necessary if we want to use standard-version on local or Colab.
     ```bash
      !npm install --save-dev standard-version
      ```
   - Edit package.json to add standard-version in the scripts. The file should look like this:
      ```json
      {
        "name": "versioning-workflow",
        "version": "1.0.0",
        "description": "In this repository...",
        "main": "index.js",
        "scripts": {
          "test": "echo \"Error: no test specified\" && exit 1",
          "release": "standard-version"
        },
        "repository": {
          "type": "git",
          "url": "git+https://github.com/jcaste05/versioning-workflow.git"
        },
        "keywords": [],
        "author": "",
        "license": "ISC",
        "bugs": {
          "url": "https://github.com/jcaste05/versioning-workflow/issues"
        },
        "homepage": "https://github.com/jcaste05/versioning-workflow#readme",
        "devDependencies": {
          "standard-version": "^9.5.0"
        }
      }
      ```
   - Add a config file to choose which commits will appear in the changelog. See [examples of convetional commits](#examples-of-conventional-commits)
      ```js
      module.exports = {
      types: [
        { type: 'feat', section: 'Features' },
        { type: 'fix', section: 'Bugs fixed' },
        { type: 'BREAKING CHANGE', section: 'Major changes' },
        { type: 'chore', section: 'Small changes' },
        { type: 'docs', section: 'Documentation' },
        { type: 'test', section: 'Tests' }
      ]
      };
      ```
      You can create it with:
     ```bash
     !echo "module.exports = { types: [{ type: 'feat', section: 'Features'}, { type: 'fix', section: 'Bugs fixed'}, { type: 'BREAKING CHANGE', section: 'Major changes'}, { type: 'chore', 'section': 'Small changes'}, { type: 'docs', section: 'Documentation'}, { type: 'test', section: 'Tests'}] };" > .versionrc.js
     ```
     Verify that you created it correctly:
     ```bash
     !cat .versionrc.js
     ```
   - Push the new files:
     ```bash
     !git add .
     !git commit -m "chore: node.js project and configuration for standard-release added."
     !git push https://<<user_name>>:<<PersonalAccesToken>>@github.com/<<user_name>>/versioning-workflow.git main
     ```
  4. **First use of npm standard-version**:
       - We can see what standard-version will do without making any change with the command:
           ```bash
           !npx standard-version --dry-run
           ```
           It will print something like this:
           ```plaintext
            ✔ bumping version in package.json from 1.0.0 to 1.0.1
            ✔ bumping version in package-lock.json from 1.0.0 to 1.0.1
            ✔ created CHANGELOG.md
            ✔ outputting changes to CHANGELOG.md
            ✔ committing package-lock.json and package.json and CHANGELOG.md
            ✔ tagging release v1.0.1
            ℹ Run `git push --follow-tags origin main && npm publish` to publish
           ```
           This report that standard-version will bump current version (1.0.0) to the version 1.0.1. Also, it will create CHANGELOG.md that will store all changes and versions. The files CHANGELOG.md, package.json and package-lock will be overwritten with the new version. The git tag v1.0.1 is created too.
      - Because everything will work properly, we will run standard-version:
           ```bash
           !npx standard-version
           ```
      - Push the changes caused by standard-version:
        ```bash
           !git push --follow-tags https://<<user_name>>:<<PersonalAccesToken>>@github.com/<<user_name>>/versioning-workflow.git main
        ```
### 2. Create GitHub action for automating versioning.
   1. **Go to Actions on github and select "_new workflow_" and "_set up a workflow yourself_".**
   2. **Create the workflow writing this yaml file:**
      ```yml
      name: Release Workflow

      on:
        push:
          branches:
            - main
      
      jobs:
        release:
          runs-on: ubuntu-latest
      
          permissions:
            contents: write
      
          steps:
            - name: Checkout code
              uses: actions/checkout@v2
      
            - name: Set up Node.js
              uses: actions/setup-node@v2
              with:
                node-version: '16'
      
            - name: Install dependencies
              run: npm install
      
            - name: Configure Git
              run: |
                git config --global user.name <<user_name>>
                git config --global user.email <<user_email>>
      
            - name: Run release
              run: npm run release
              env:
                GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
            - name: Push changes and tags
              run:
                git push --follow-tags origin main
              env:
                GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      ```
      This yaml indicates that when a push is done, github will automatically launch an instance with ubuntu, clone the repository, install Node.js and the dependencies, run standard-version with npm run release and push the changes on CHANGELOG.md and the rest on the repository creating the corresponding tag. This file will be saved in ./.github/workflows/.

### 3. Create a script on Colab and push the changes to see the workflow.
   1. **Update with "_!git pull_" the repository on Colab or clone it again.**
   2. **Create an example file**:
      ```python
      %%writefile calculator.py
      def sum(a, b):
        return a + b
      ```
   3. **Commit the changes and push:**
      ```bash
      !git add calculator.py
      !git commit -m "feat: calculator.py created with function called sum" -m "The function sum takes two numbers and returns their sum."
      !git push https://<<user_name>>:<<PersonalAccesToken>>@github.com/<<user_name>>/versioning-workflow.git main
      ```
   4. **Go to Actions on GitHub to check the process of auto-versioning. The version will be bumped automatically!**
      
### 4. Create an action that checks the functions defined on calculator and the code format.
   1. **Refresh the repo and create the test file "_test_calculator.py_":**
      ```python
      %%writefile test_calculator.py

      from calculator import sum
      
      def test_sum():
          assert sum(2, 3) == 5
          assert sum(-1, 1) == 0
          assert sum(0, 0) == 0
      ```
   2. **Push the changes. Now the repository has test files to run with pytest.**
   3. **Create the GitHub action that runs pytest and checks the code format with flake8.**
      - Go to Actions on GitHub and create a new workflow. The yaml should be like this one:
        ```yml
        name: Python Tests Lint

         on:
           push:
             branches:
               - main 
             paths:
               - '**/*.py'  # Workflow only is ejecuted if there are changes on scripts *.py
         
         jobs:
           test:
             runs-on: ubuntu-latest
         
             steps:
               - name: Checkout code
                 uses: actions/checkout@v2
         
               - name: Set up Python
                 uses: actions/setup-python@v2
                 with:
                   python-version: '3.10' 
         
               - name: Install dependencies
                 run: |
                   python -m pip install --upgrade pip
                   pip install pytest flake8
         
               - name: Run tests
                 run: |
                   pytest
         
               - name: Check code style with flake8
                 run: |
                   flake8 .
        ```
        This workflow is executed when a push modify scripts *.py. First, install python and the libraries pytest and flake8. Then, it runs pytest and flake8. If some test failed or flake8 detect an error with the code format, the workflow will failed.
### 4. The repository has already been configured!
   1. **You can add more scripts and test that could fail to see how the workflows work.**
   2. **Use the library [black](https://black.readthedocs.io/en/stable/index.html) to format your code automatically.**
        
      
   


## Examples of conventional commits
The general basic structure for a conventional commit is x(scope): description where:
- x denote the kind of the change. For example: fix, feature, docs, style...
