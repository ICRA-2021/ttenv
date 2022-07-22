FROM robinlab/robot-libs:20.04

RUN pip install pyyaml filterpy scikit-image

RUN git clone https://github.com/ICRA-2021/ttenv.git

