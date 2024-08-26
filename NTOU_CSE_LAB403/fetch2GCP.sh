sftp -i /home/pi/.ssh/id_rsa pi@35.194.132.151 <<EOF
put -r main/video ar0
exit
EOF
