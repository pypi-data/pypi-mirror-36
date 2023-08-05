# mapctf - map coordinate transform
# 此模块用于百度坐标系(bd-09)、
# 火星坐标系(国测局坐标系、gcj02、高德)、
# WGS84坐标系(google)的相互转换，
# 仅使用Python标准模块，无其他依赖。
python3 setup.py sdist bdist_wheel
# for test.pypi
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ coordTransform
# for pypi
python -m twine upload dist/*
pip install mapctf
# Usage
import mapctf
ctf.baidu2google(lng, lat)
