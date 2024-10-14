# versioning-workflow
In this repository, automatic versioning is implemented through the use of conventional commits and npm standard-version. Also, the use of GitHub actions is exemplified to verify code writing standards and the use of unit tests with pytest.

## Overview

This repository is designed with an automated versioning workflow and CI/CD pipeline using GitHub Actions. It includes:

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
   - Add a config file to choose which commits will appear in the changelog. See [examples of convetional commits](##Examples-of-convetional-commits)
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
     
   


## Examples of conventional commits
