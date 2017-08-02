# BoerOPS

## Usage

### Pyhon 3.5
```bash
安装Python
> https://www.python.org/downloads/release/python-353/
安装Python包管理器pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
安装Python虚拟环境工具virtualenv
pip install virtualenv
# Check
which virtualenv
```

### Node / NVM
```bash
NodeJS版本管理器
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.2/install.sh | bash
source ~/.bashrc
# or
source ~/.zshrc
# 安装指定版本NodeJS
nvm install 6.10.3 --lts
# Check
which npm
```

### Run Dev
```bash
git clone git@github.com:BoerOPS/BoerOPS.git
# Node环境
cd BoerOPS/fe
npm install
npm run build
# Python环境
cd ..
virtualenv venv
source venv/bin/active
pip install -r requirements.txt
python runserver.py
```

---

#### 「Stay hungry. Stay foolish.」