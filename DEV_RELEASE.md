# Media Library Reader -- Code Release Process

## Contents Outline 1

 * Introduction
 * Close Out Development Branch
   * Verify Repo Status
   * Run Code Tests
   * Create Release Issue Ticket
   * Pull Request: Development Into Integration
 * Create Release In Integration Branch
   * Checkout Integration
   * Update CHANGELOG.md
   * Update pyproject.toml
   * Build Test Package
   * Upload Package To Test Package Repository
   * Commit File Changes
   * Pull Request: Integration Into Main
 * Finalize Release In Main Branch
   * Checkout Main
   * Create Annotated Tag
   * Push Local Tag To Remote Server
   * Upload code package to main repository
 * Pull Changes Back To Development
   * Checkout Integration
   * Merge In Main
   * Checkout Development
   * Merge In Integration
 * Finalization
   * Close Issue Ticket

## Introduction

The following is a procedure outline for doing a full release of the medialibrary Python module.
It covers pushing changes from the `development` branch to the `integration` branch, building 
a Python package, pushing the `integration` branch to the `main` branch, and then pulling all 
of the accumulated changes and tagging back down to the `development` branch.

### Miscellaneous Notes

 * Version numbers follow the major.minor.patch methodology
   * Minor version updates can add functionality, but they
  should not break existing functionality
 * This procedure follows a model where there are no beta stages to
   the release, or additional testing of the software package after it is
   initially built.
 * This assumes a simple git repo setup where everyone commits to the same remote server.
   * The remote server is referred to as the `remote`, even though by default in
     the configuration it is probably referred to as `origin`.


## Close Out Development Branch

Confirming all development work is done, and getting the repository ready to build a release.

| Branch | Local vs. Remote | Change Action |
|--------|-----------------|----------------|
| `development` | `local` | Checkout `development` |
| `development` | `remote -> local`  | Pull changes from remote |
| `development` | `remote` | Create PR from `development` to `integration` |
| `development` | `remote` | Merge PR |

### Verify Repo Status

The release engineer should be in the development branch, and it should be clean and clear
of untracked files or changed files.  All developer code commits should be completed, 
and pushed, all developer level pull requests that are slated for this release should be 
merged.  There should be a final pull from the remote to ensure the local development branch
is up to date.

```
git checkout development
git pull origin
```

### Run Code Tests

Run the code test suite.  All results should come back clean.

### Create Release Issue Ticket

Create the issue ticket that will identify the release.  The ticket should list all
changes going into the release.

### Pull Request: Development Into Integration

Create a Pull Request pulling the remote development branch into the remote
integration branch.


## Create Release In Integration Branch

Making the necessary release changes to build a new package, and then preserving those changes.

| Branch | Local vs. Remote | Change Action |
|--------|-----------------|----------------|
| `integration` | `local`  | Checkout `integration` |
| `integration` | `remote -> local` | Pull changes from remote |
| `integration` | `local`  | Update CHANGELOG.md |
| `integration` | `local`  | Update pyproject.toml |
| `integration` | `local` | Commit file changes |
| `integration` | `local -> remote` | Push local changes |
| `inbtegration` | `remote` | Create PR from `integration` to `main` |
| `integration` | `remote` | Merge PR |

### Checkout Integration

Branch `integration` should now have accumulated changes just merged from `development`.

```
git checkout integration
git pull
```

### Update CHANGELOG.md

Change the `CURRENT` block to reflect the desired release version.

### Update pyproject.toml

Change the `version` attribute of the pyproject.toml file

### Build Test Package

Build a software package (.tar.gz file or .whl file or both)

### Upload Package to Test Package Repository

Upload the package to the test package repository website.  The upload should
be clean, with no errors.

If there is a failure, fix the issue and try again.

### Commit File Changes

```
git add CHANGELOG.md pyproject.toml
git commit -m "[ticket_id] Release (version)"
git push origin
```

### Pull Request: Integration Into Main

Merge the `integration` branch into the `main` branch on the remote server.

## Finalize Release In Main Branch

Finalizing the release at the repository level.

| Branch  | Local vs. Remote | Change Action |
|---------|------------------|---------------|
| `main`  | `local`          | Checkout `main` |
| `main`  | `remote -> local`  | Pull `main` updates |
| `main`  | `local` | Create annotated version tag |
| `main`  | `local -> remote` | Push tag to origin |


### Checkout Main Branch

```
git checkout main
git pull
```

### Create Annotated Tag

```
git tag -a v(version_no) -m "version (version_no)"
```

### Push Local Tag To Remote Server

```
git push origin v(version_no)
```

### Upload Package to Staging And Production 

Upload the software package to the staging repository.  Once testing is complete, upload
the package to the production repository.

## Pull Changes Back To Development

Take the changes from the `integration` and `main` branches, and pull them all down to 
the `development` branch.


| Branch        | Local vs. Remote | Change Action |
|---------------|------------------|---------------|
| `integration` | `local`   | Checkout `integration` |
| `integration` | `remote -> local` | Pull down changes |
| `main -> integration` | `local` | Merge `main` into `integration` |
| `integration` | `local -> remote` | Push `integration` to remote |
| `development` | `local` | Checkout `development` |
| `development` | `remote -> local` | Pull down changes |
| `integration -> development` | `local` | Merge `integration` into `development` |
| `development` | `local -> remote` | Push `development` to remote |

### Checkout Integration

Checkout the integration branch, and do a pull to make sure it's current.

```
git checkout integration
git pull
```

### Merge In Main

Merge the `main` branch into `integration`, and then push the result 
to the remote server.  This will effectively put the annotated tags that were 
made in the `main` branch into the `integration` branch.

```
git merge main
git push
```

At the end of this operation, `integration` and `main` should be identical.

```
git diff main integration
```


## Checkout Development

Checkout the `development` branch, and do a pull to make sure it's current.

```
git checkout development
git pull
```

## Merge In Integration

Merge the `integration` branch into `development`, and then push the
result to the remote server.  This will pull in the annotated tags 
from `main`, and the file changes to CHANGELOG.md and pyproject.toml 
from `integration` into the `development` branch.


```
git merge integration
git push
```

At the end of this operation, `development` and `integration` and `main` should all
be identical.


```
git diff integration development
git diff main development
```

## Finalization

### Close Issue Ticket

Close the issue ticket that was created for the release.

