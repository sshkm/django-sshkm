#!/bin/bash

# check parameter count
if [ "$2" == "" ]; then
    echo "usage: $0 <tag> <message>"
    exit 1
fi

# check correct working dir
if [ ! -d .git -a ! -f setup.py ]; then
    echo "please run this script from project base directory"
    exit 2
fi

# check if rpmbuild is installed
which rpmbuild >/dev/null 2>&1
if [ $? -ne 0 ]; then
    yum -y install rpmdevtools rpmlint
fi

# check if build environment is created
if [ ! -d ~/rpmbuild ]; then
    rpmdev-setuptree
fi

# predefine variables
TAG=$1
MESSAGE="$2"
GITDIR=$(pwd)
GITREPO=https://github.com/sshkm/django-sshkm.git
TEMPDIR=/tmp/sshkm-build
SPEC=rpmbuild/SPECS/sshkm.spec

# cleanup temp dir
rm -rf $TEMPDIR
mkdir -p $TEMPDIR

# clone git repo
cd $TEMPDIR
git clone $GITREPO
cd $TEMPDIR/django-sshkm

# get RPM release
RELEASE=$((($(grep "Release:" $SPEC | awk '{print $2}' | awk -F '%' '{print $1}')+1)))

# verify settings
echo "--------------------------------------------------------------"
echo "TAG: $TAG"
echo "MESSAGE: $MESSAGE"
echo "RPM RELEASE: $RELEASE"
echo ""
echo "---- please press enter to continue"
echo "--------------------------------------------------------------"
read
echo ""

# set version in setup.py
sed "s/version = .*/version = $TAG/g" setup.py | grep version
#sed -i "s/version = .*/version = $TAG/g" setup.py

# set version and releas in SPEC file
sed "s/Version:\t.*/Version:\t$TAG/g" $SPEC | grep Version
#sed -i "s/Version:\t.*/Version:\t$TAG/g" $SPEC
sed "s/Release:\t.*/Release:\t$RELEASE%{?dist}/g" $SPEC | grep Release
#sed -i "s/Release:\t.*/Release:\t$RELEASE%{?dist}/g" $SPEC

# create tarball for rpmbuild
RPMSRC=$TEMPDIR/rpmbuild/SOURCES
mkdir -p $RPMSRC
cp -a rpmbuild/SOURCES/sshkm-master $RPMSRC/
mv $RPMSRC/sshkm-master $RPMSRC/sshkm-$TAG
cd $RPMSRC
tar czf ~/rpmbuild/SOURCES/sshkm-${TAG}.tar.gz sshkm-$TAG/
cd $TEMPDIR/django-sshkm
tar tf ~/rpmbuild/SOURCES/sshkm-${TAG}.tar.gz

# cleanup temp dir
rm -rf $TEMPDIR

# commit and push last modifications to git repo
#git commit -a -m "$MESSAGE"
#git push

# create tag and push it to git repo
#git tag -a $TAG -m "$MESSAGE"
#git push origin $TAG


