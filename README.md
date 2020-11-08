# Sapient France - Certifications

This repository contains code related to our Certifications.

The objective are:

- Getting certifications information
- Sanitizing/checking them
- Storing them in a reliable and stable format in S3

# Pattern

- One Function that encapsulates the logic of retrieving content

And other functions to call it:
- One Function that exposes its result live (and fallback / cache ?)
- One Function that runs daily and store its result
- One Function that runs every hour and check if everything succeeds or not
