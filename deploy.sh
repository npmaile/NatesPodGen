#!/usr/bin/env bash
echo "Welcome to Nate's podcast generator"
WorkingDirectory=$(pwd)
echo -e "first things first, what is the fully qualified domain name you wish to host this podcast on\n format: subdomain.website.tld"
read FQDN

while true; do
	read -p "confirm that $FQDN is correct [y/n]" answer
	case $answer in
		[Yy]* ) break;;
		[Nn]* ) read "please correct your fqdn" FQDN;;
		* ) echo "Please anser with a y or an n";;
	esac
done

mkdir config
mkdir site
mkdir site/images
mkdir site/episodes
cat templates/podcast.conf | sed "s/\$FQDN/$FQDN/g" | sed "s|\$workingdirectory|$WorkingDirectory|g" > config/podcast.conf

cat templates/feed.ini  | sed "s/\$FQDN/$FQDN/g" | sed "s|\$workingdirectory|$WorkingDirectory|g" > feed.ini
cat templates/general.conf > config/general.conf

echo -e "if there were no errors, the process is complete\
	\nThe next steps are as follows\
	\n1. add the nginx directive of inclucde $WorkingDirectory/config/podcast.conf\
	\n2. Set up ssl certificates for this site (letsencrypt has a script that will do this automagically)\
	\n3. edit the feed.ini file to have information for the global configuration
	\n4(optional if you want to manually add episodes) run the addepisode script to add your episodes)"
