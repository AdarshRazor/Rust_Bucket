#!/bin/sh

adddate() {
    while IFS= read -r line; do
        printf '%s %s\n' "$(date "+%Y-%m-%d %H:%M:%S")" "$line";
    done
}

ip=${1}

echo "Cluster IP: ${ip}" >> adddate() >> samsung.log
echo "curl -X GET --header 'Accept: application/json' 'https://${ip}/api/serverInfo'" >> adddate() >> samsung.log
curl -X GET --header 'Accept: application/json' 'https://${ip}/api/serverInfo' >> samsung.json

N=0
echo "while [ $N -ne 1 ]" >> adddate() >> samsung.log
while [ $N -lt 1 ]
do
   echo "curl -X GET --header 'Accept: application/json' 'https://${ip}/api/serverInfo'" >> adddate() >> samsung.log
   curl -X GET --header 'Accept: application/json' 'https://${ip}/api/serverInfo' >> samsung.json
   if grep -o ACTIVE samsung.json
   then
   echo "Cluster state is ACTIVE !!" >> adddate() >> samsung.log
   N=2
   else
   echo "sleeping for 10 sec" >> adddate() >> samsung.log
   sleep 10
   fi
done

echo "Ending While Statement" >> adddate() >> samsung.log
echo "Done" >> adddate() >> samsung.log
