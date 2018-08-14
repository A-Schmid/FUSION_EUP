echo "FUSION setup starting"
echo "setting up udev rules..."
cp additional_files/udev/* /etc/udev/rules.d/

echo "creating directory for daemons..."
mkdir /usr/local/bin/FUSION

echo "copying daemons to said directory..."
cp additional_files/daemons/* /usr/local/bin/FUSION

if [ "$1" = "no-udev" ]
then
	echo "skipped reload of udev rules."
else
	echo "reloading udev rules..."
	sh additional_files/scripts/reload_udev.sh
fi

echo "FUSION setup done"
