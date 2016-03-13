#!/usr/bin/env bash
git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "kylinfish" ];
        then
                GIT_COMMITTER_NAME="wujuguang";
                GIT_AUTHOR_NAME="wujuguang";
                GIT_COMMITTER_EMAIL="1154545932@qq.com";
                GIT_AUTHOR_EMAIL="1154545932@qq.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD