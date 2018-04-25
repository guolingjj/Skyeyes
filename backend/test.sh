#!/bin/bash

md_str=$1
for i in $(seq 1 30)
do
    ssh_pid=`ps -ef|grep $md_str|grep -v sshpass|grep -v test.sh|grep -v grep |awk '{print $2}'`

    if [ "$ssh_pid" = "" ]; then
    continue
    else
        today=`date "+%Y%m%d"`
        today_audit_dir="logs/audit/$today"
        if [ -d $today_audit_dir ];
        then
            echo 'start tracker log'
        else
            echo lg54jj55 |sudo -S mkdir -p $today_audit_dir

        fi;
        echo lg54jj55 |sudo -S /usr/bin/strace -ttt -p $ssh_pid -o "$today_audit_dir/$md_str.log"
        echo $today_audit_dir
        break;
    fi;
done;
