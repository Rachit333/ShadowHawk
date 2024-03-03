mkdir -p ~/python
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xzf Python-3.10.0.tgz
cd Python-3.10.0
./configure --prefix=$HOME/python
make
make install
~/python/bin/python3 --version
