python setup sdist
git commit -a Changelog
git tag $VERSION
git push origin
python setup sdist
twine upload build/*$VERSION.tar.gz
