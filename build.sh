#!/bin/sh
set -euo pipefail
pushd WORK > /dev/null
VER="$(git describe --tags)"
declare -a VERARR=(${VER/-/ })
popd
VERARR[1]="$(date '+%Y%m%d').${VERARR[1]}"
tar --transform "s/WORK/postsrsd-${VERARR[0]}/" -cjf SOURCES/postsrsd-${VERARR[0]}.tar.bz2 WORK/
sed -e "s/%VERFULL%/${VER}/" -e "s/%VERSION%/${VERARR[0]}/" \
	-e "s/%RELEASE%/${VERARR[1]/-/.}/" SPECS/postsrsd.spec.in > SPECS/postsrsd.spec
rpmbuild --define 'dist .apnscp'  --define "_topdir `pwd`" -ba SPECS/postsrsd.spec
