# The first step to CCC_Journey


## 초기 설정

git config --global user.name "github 이름"

git config --global user.email "github 이메일"

git config --list


## local 저장소에서

git init

git add . 

git status

git commit -m "커밋메시지"

git remote add origin {github 주소}

git remote -v 

git push origin main



## github에서

git pull origin main

코드를 local 저장소에서 수정 후 다시 github으로 전송함
