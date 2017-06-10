import requests
import sys
import git
from os import getenv

class Plzrebase:
    def __init__(self):
        self.threshold = int(getenv('PLZREBASE_THRESHOLD', '50'))
        self.master = getenv('PLZREBASE_BRANCH_TO_COMPARE', 'master')
        self.webhook = getenv('PLZREBASE_SLACK_WEBHOOK_URL')
        self.channel = getenv('PLZREBASE_SLACK_CHANNEL')
        self.excludes = getenv('PLZREBASE_BRANCH_PREFIX_EXCLUDE', '').split(',')

        self.project = getenv('CI_PROJECT_PATH')
        self.branch = getenv('CI_COMMIT_REF_NAME')
        self.author = getenv('GITLAB_USER_EMAIL')

        self.repo = git.Repo('.')
        try:
            self.active = self.repo.active_branch.name
        except TypeError:
            self.active = getenv('CI_COMMIT_SHA')

        self.url = getenv('CI_PROJECT_URL')

        self.pipeline = '<{0}/pipelines/{1}|#{1}>'.format(
            self.url, getenv('CI_PIPELINE_ID')
        )
        self.commit = '<{0}/commits/{1}|{1:.8}>'.format(
            self.url, getenv('CI_COMMIT_SHA')
        )


    def set_diff(self):
        commits = self.repo.iter_commits(
            f'{self.active}..{self.master}',
            max_count=self.threshold*2,
        )
        self.diff = len(list(commits))


    def complain_over_threshold(self):
        if self.diff > self.threshold:
            self.slack()
            print(f'Branch is {self.diff} commits behind. Please rebase.')
            sys.exit(1)
        else:
            print(f'Branch is {self.diff} commits behind. All good.')

    def complain_excluded(self):
        for prefix in self.excludes:
            if self.branch.startswith(prefix):
                print(f'Branch {self.branch} is excluded.')
                sys.exit(0)

    def slack(self):
        if not self.webhook:
            return

        text = f'<{self.url}|{self.project}> is {self.diff} commits behind'
        fields = [
            ('Pipeline', self.pipeline),
            ('Commit', self.commit),
            ('Author', self.author),
            ('Branch', self.branch),
        ]

        payload = {'text': text}
        if self.channel:
            payload['channel'] = self.channel

        payload['attachments'] = [{'fields': 
                [dict(title=k, value=v, short=True) for k, v in fields]
        }]

        r = requests.post(self.webhook, json=payload)
        r.raise_for_status()


    def complain(self):
        self.complain_excluded()
        self.set_diff()
        self.complain_over_threshold()


def main():
    plz = Plzrebase()
    plz.complain()


if __name__ == '__main__':
    main()
