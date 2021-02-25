Run this command at only tracker end
ipconfig /all > c:/ip.txt | type c:/ip.txt

run this command at each peer end
ipconfig /all > c:/host_ip.txt | type c:/host_ip.txt

Check ip.txt file, and host_ip.txt file at the specified location in the code(c:\ip.txt and c:\host_ip.txt)

Run tracker.py

Run peer.py

perform the operations available in the meenu of peer-end

All the files to be shareable are included in rfc folder

All the new files will be downloaded in rfc folder at downloading peer end

Make sure that tracker and all peers are conected to same wifi

The file ip.py is reflecting the IP extraction code seperately