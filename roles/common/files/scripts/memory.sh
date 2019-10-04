#free
#              total        used        free      shared  buff/cache   available
#Mem:       49296728      416732    48290640         524      589356    48632744
#Swap:       2129916           0     2129916

free -h | gawk  '/Mem:/{print "Total: "$2}'
free -h | gawk  '/Mem:/{print "Used: "$3}'
free -h | gawk  '/Mem:/{print "Free: "$4}'