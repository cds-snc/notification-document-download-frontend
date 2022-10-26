
**The document-download-frontend app has been removed from GC Notify.**

Consequently we have archived this repository.

# document-download-frontend
GOV.UK Notify Document Download frontend user application

## Updating application dependencies

`requirements.txt` file is generated from the `requirements-app.txt` in order to pin
versions of all nested dependencies. If `requirements-app.txt` has been changed (or
we want to update the unpinned nested dependencies) `requirements.txt` should be
regenerated with

```
make freeze-requirements
```

`requirements.txt` should be committed alongside `requirements-app.txt` changes.
