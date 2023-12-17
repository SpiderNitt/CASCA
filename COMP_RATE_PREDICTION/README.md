Enable venv
```bash
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
```

Update cpu stress script
```bash
cp update_cpu.py ./lib/python3.9/site-packages/stressinjector/cpu.py
```
