# Streamlit Label Kit

Streamlit component for general labeling task


## Installation instructions

```sh
pip install streamlit-label-kit
```

or

1. git clone this repo.
2. build frontend as following

```sh
cd streamlit_label_kit/LabelToolKit/frontend
yarn install
yarn build
```
3. activate your virtual environment
4. pip install -e .

## Example Uses
Checkout example/demo.py

run by 
```bash
pip install streamlit-label-kit matplotlib
streamlit run --server.headless True --server.fileWatcherType none example/demo.py 
```

## License

Unless otherwise stated, all source code and documentation are under the [GPL-2.0]. A copy of this license is included in the [LICENSE](LICENSE) file.

This project is inspired by and modified the content from following third-party sources:

| Project | Modified | License |
| --- | --- | --- |
| [hirune924/Streamlit-Image-Annotation](https://github.com/hirune924/Streamlit-Image-Annotation) | Yes | Apache-2.0 license |
