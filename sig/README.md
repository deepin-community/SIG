# SIG Setup Guide

## SIG setup

To set up a SIG, in [this SIG repository under deepin-community on Github](https://github.com/deepin-community/SIG/), create a folder in this directory, place files in it according to the requirements, and submit a Pull Request to apply for SIG setup. The SIG board will review the pull request of your application. When the pull request is merged, the SIG is created.

### Requirements

Before setup, make sure your group meets the following requirements:

- The topic and activities must be related to deepin and/or DDE.
- Keep activities public.
- Have outputs that can be public to the whole deepin community.
- At least two members (It is recommended to have at least five members).

### Preparation

To create a SIG, you need to prepare:

- SIG group name
- Group ID (lowercase letters and hyphens only)
- Reason for creation
- Group profile
- Locations and objectives of activities
- Public discussion channel
- GitHub accounts of group leaders and members

When you're ready, move on to the next steps.

### Steps

Fork this repository, copy the files in the `.template` folder in this directory to a new folder named with your group ID, and edit the files in it accordingly, finally push the changes and submit a pull request.

When editing the template files, pay attention to the description in them. Information in `metadata.yml` will be public, and the members listed there will be invited to join the deepin-community organization.

When submitting a pull request, please use `[New SIG Proposal] SIG name` as its title, and write down the reason for creation and the GitHub accounts of group leaders as the following example.

``` markdown
## Reason

Write down the setup reason for your SIG here.

## Create a repository

My SIG needs a repository under the deepin-community organization:

- sig-group-id
- ...

(Note: If you do not need the repository, delete this "Create a repository" section directly.)
```

If you or other group members are not familiar with the pull request workflow on GitHub, open an issue and leave the above information in it to request help from the SIG board.

Note: Although SIGs can create repositories under deepin-community, the group activities are not required to be carried out under this GitHub organization. You can choose any suitable and public location to manage SIG activities, such as other GitHub organizations, or other platforms such as Gitee.

### Subsequent process

After a pull request is submitted, the SIG board gives feedback within three working days. If there is any feedback, the applicant or other group members should discuss and agree with the board in the pull request.

When the pull request is finally merged, the SIG is created. If you do not want to create the SIG before the final setup, just close the corresponding pull request.

## SIG Change Request

To update the SIG information, edit the files in your group folder, and submit a pull request. After being reviewed by the SIG board, the modifications are merged.

If you or other group members are not familiar with the pull request workflow on GitHub, open an issue and write down the necessary info to request help from the SIG board. 
