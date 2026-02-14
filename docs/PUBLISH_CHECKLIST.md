# GitHub Publish Checklist

## 1) Repository metadata

- [ ] Update repository name and description
- [ ] Add topics/tags (django, education, university, rbac, python)
- [ ] Add project website or demo link

## 2) README finalization

- [ ] Replace `USERNAME/REPO` placeholders
- [ ] Update clone URL
- [ ] Add screenshots under `docs/screenshots/`
- [ ] Add demo video/GIF link
- [ ] Confirm tests badge value

## 3) Code quality

- [ ] Run `python manage.py check`
- [ ] Run `python manage.py test`
- [ ] Ensure no debug-only code remains
- [ ] Verify migrations are up-to-date

## 4) Clean repository state

- [ ] Do not commit `db.sqlite3`
- [ ] Do not commit `media/` generated files
- [ ] Do not commit `__pycache__/` or `.pyc`

## 5) Final push

- [ ] Create clean commit message
- [ ] Push to `main`
- [ ] Create first release tag (optional)
- [ ] Share project link in portfolio/CV/LinkedIn
