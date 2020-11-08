# Sapient France - Certifications

![Unit tests status](https://img.shields.io/github/workflow/status/xebia-france/certifications/Kubernetes%20Certifications%20unit%20tests?label=Unit%20tests)

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
