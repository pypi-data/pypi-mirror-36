python setupi.py sdist
git commit ChangeLog
git tag $VERSION
git push origin
python setup sdist
twine upload build/*$VERSION.tar.gz
