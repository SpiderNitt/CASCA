# Creating a mountable disk
echo "Making directory for RAM Disk"
mkdir /mnt/pktramdisk
echo "Mounting /mnt/pktramdisk"
mount -t tmpfs -o rw,size=256M tmpfs /mnt/pktramdisk