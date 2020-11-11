# Sapient France - Certifications

[![Unit tests status](https://img.shields.io/github/workflow/status/xebia-france/certifications/Kubernetes%20Certifications%20unit%20tests?label=Unit%20tests&logo=github)](https://github.com/xebia-france/certifications/actions?query=workflow%3A%22Unit+Tests%22+branch%3Amaster)
![Lint & CodeStyle status](https://img.shields.io/github/workflow/status/xebia-france/certifications/Lint%20Code%20Base?label=Lint%20%26%20CodeStyle&logo=github)
![Last commit](https://img.shields.io/github/last-commit/xebia-france/certifications?logo=github)
![Code quality (Codacy)](https://img.shields.io/codacy/grade/1f244174349d443595675928999e0d1c?label=Code%20quality&logo=codacy)

![Tests - Code coverage (on Codacy)](https://img.shields.io/codacy/coverage/1f244174349d443595675928999e0d1c?label=Tests%20coverage&logo=codacy)
![Tests - Code coverage (on Coveralls)](https://img.shields.io/coveralls/github/xebia-france/certifications?label=Tests%20coverage&logo=coveralls)
[![Tests - Code coverage (on Codecov)](https://img.shields.io/codecov/c/github/xebia-france/certifications?label=Tests%20-%20Code%20coverage&logo=codecov)](https://codecov.io/gh/xebia-france/certifications)

[![Slack channel](https://img.shields.io/badge/Slack-%23xebia--data--driven-red?style=social&logo=slack&logoColor=black)](https://xebiafr.slack.com/archives/C9D5E48F2)

This repository contains code related to our Certifications.

The objective are:

- Getting certifications information
- Sanitizing/checking them
- Storing them in a reliable and stable format in S3

## Coding practices

### Lint

Code is linted using flake8.

### Codestyle

Code is formatted using Black.

## Pattern

- One Function that encapsulates the logic of retrieving content

And other functions to call it:
- One Function that exposes its result live (and fallback / cache ?)
- One Function that runs daily and store its result
- One Function that runs every hour and check if everything succeeds or not
