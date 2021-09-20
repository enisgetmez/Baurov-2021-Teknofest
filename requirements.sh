sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install nano -y
sudo apt-get install python3-pip -y
sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/nvidia-tegra.conf" -y
sudo ldconfig 
sudo apt-get install build-essential cmake git unzip pkg-config -y
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev -y
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev -y
sudo apt-get install libgtk2.0-dev libcanberra-gtk* -y
sudo apt-get install python3-dev python3-numpy python3-pip -y
sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev -y
sudo apt-get install libtbb2 libtbb-dev libdc1394-22-dev -y
sudo apt-get install gstreamer1.0-tools libv4l-dev v4l-utils -y
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev -y
sudo apt-get install libavresample-dev libvorbis-dev libxine2-dev -y
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev -y
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev -y
sudo apt-get install libopenblas-dev libatlas-base-dev libblas-dev -y
sudo apt-get install liblapack-dev libeigen3-dev gfortran -y
sudo apt-get install libhdf5-dev protobuf-compiler -y
sudo apt-get install libprotobuf-dev libgoogle-glog-dev libgflags-dev -y
export PATH=/usr/local/cuda-10.2/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
sudo apt-get install qt5-default -y
