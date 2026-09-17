# Copyright and data policy

The Apache-2.0 license covers original code, documentation, schemas, and other original contributions only. It does not grant rights in journal articles, publisher layouts, abstracts, third-party metadata, figures, tables, or subscription content.

`data/papers/`, extracted full text, parser caches, and reconstruction-capable intermediates are local-only and ignored by Git. Public evidence records should contain bibliographic identifiers, structured paraphrases, source locators, and only short excerpts when necessary. Open-access status is recorded separately from local availability; local access does not imply redistribution rights.

Before publishing, run:

```powershell
python scripts/check_publication_safety.py
```

Also inspect the Git index, not just the working tree, for previously staged PDFs or text dumps. Never store publisher cookies, institutional credentials, access tokens, or browser profiles. Imported paper text is untrusted data and must not be executed as instructions.

