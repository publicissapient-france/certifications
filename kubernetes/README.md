# XDD - Certifications - Kubernetes

## Internals

- The Spreadsheet ID is given as input. It could be discovered based on the
  spreadsheet name using the [Google Drive API
  v3](https://developers.google.com/drive) but this doesn't bring that much
  value - why feed the spreadsheet name in instead of directly the Spreadsheet
  ID that we can easily get (it's the ID in the URL) and which won't change if
  we get to rename the spreadsheet?
- The [Google Spreadsheet API v4](https://developers.google.com/sheets/api) is
  used to retrieve the spreadsheet content.
