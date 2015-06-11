#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from base import PluginBase

ISSUE_API = "https://api.github.com/repos/{org}/{repo}/issues"
REPO_API = "https://api.github.com/orgs/{org}/repos"


class GithubIssue(PluginBase):

    @staticmethod
    def test(data, bot):
        return 'issue' in data['message']

    @staticmethod
    def handle(data, bot, kv, app):
        org_name = app.config.get('ORG_NAME', 'python-cn')
        repos = requests.get(REPO_API.format(org=org_name)).json()
        rv = ''
        for repo in repos:
            repo_name = repo['name']
            issues_count = repo['open_issues_count']
            if issues_count != 0:
                issues = requests.get(ISSUE_API.format(org=org_name,
                                                       repo=repo_name)).json()
                rv += '*{repo_name}\n'.format(repo_name=repo_name)
                for issue in issues:
                    rv += 'Issue {}:'.format(issue['number'])
                    rv += issue['title'].encode('utf-8') + '\n'
                    rv += issue['html_url'].encode('utf-8') + '\n'
                    rv += '\n'

        return rv if rv else 'no issue'


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.config['org_name'] = 'python-cn'
    print GithubIssue.handle(None, None, None, app)
