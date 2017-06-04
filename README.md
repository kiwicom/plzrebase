# plzrebase

A GitLab CI ready image which fails if the current branch is too outdated
from master.


Secret Variables to set:
 - `PLZREBASE_THRESHOLD` - How many commits behind are permitted, 50 by default
 - `PLZREBASE_BRANCH_TO_COMPARE` - `master` by default
 - `PLZREBASE_SLACK_WEBHOOK_URL` - Incoming webhook URL
 - `PLZREBASE_SLACK_CHANNEL` - Defaults to webhook channel


Example CI config:

```
stages:
  - build
  - test
  [ ... ]

build: 
  stage: build
  [ ... ]

plzrebase:
  stage: build
  image: kiwicom/plzrebase
  script:
   - plzrebase
```
