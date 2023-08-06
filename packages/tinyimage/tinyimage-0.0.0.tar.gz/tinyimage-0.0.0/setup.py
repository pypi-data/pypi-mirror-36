from setuptools import setup, find_packages

with open("./requirements.txt", "r") as f:
  dep_packages = f.readlines()
  # remove local install.
  dep_packages = [x.strip() for x in dep_packages if not x.startswith("-e")]
  # remove unnecessary packages.
  dep_packages = [x for x in dep_packages if not x.startswith("certifi")]

setup(
    name="tinyimage",
    version="0.0.0",
    description="a lightweight image object library",
    keywords="computer vision image",
    url="https://github.com/VisualDataIO/tinyimage",
    author="Jie Feng",
    author_email="jiefeng@perceptance.io",
    packages=find_packages("./"),
    install_requires=dep_packages,
    include_package_data=True,
    zip_safe=False)
