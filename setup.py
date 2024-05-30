import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit_label_kit",
    version="0.0.9",
    author="jinhoyi",
    description="streamlit components for general labeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmusatyalab/streamlit-label-kit",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    keywords=['Python', 'Streamlit', 'React', 'JavaScript'],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
