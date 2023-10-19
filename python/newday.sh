#!/bin/bash

# $1 is year
# $2 is day
cp ./template.py "./$1/$2.py"
sed -i '' -e "s/DAY = XX/DAY = $2/g" "./$1/$2.py"
sed -i '' -e "s/YEAR = 'XXXX'/YEAR = '$1'/g" "./$1/$2.py"



