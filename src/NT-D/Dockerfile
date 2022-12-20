FROM ubuntu:18.04
MAINTAINER SonodaKazuto

VOLUME [ '/home/project' ]

# Install packages
RUN apt update && apt upgrade -y
RUN apt install sudo zsh git nano curl -y && \
    chsh -s /usr/bin/zsh && \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" && \
    echo "linux environment setup complete"
RUN sudo apt install build-essential m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev \
    libgoogle-perftools-dev python3-dev python3-six python libboost-all-dev pkg-config -y && \
    echo "necessary packages installed"

# Load and build gem5
WORKDIR /home/project/gem5
RUN curl -s https://gem5.googlesource.com/public/gem5/+archive/525ce650e1a5bbe71c39d4b15598d6c003cc9f9e.tar.gz | \
    tar -xvz -C . && \
    scons build/X86/gem5.opt -j16 && \
    echo "gem5 built"

# Load and build NVmain
WORKDIR ..
RUN git clone https://github.com/SEAL-UCSB/NVmain
WORKDIR NVmain
COPY /nvmain-solo-build/SConscript /home/project/NVmain
RUN scons --build-type=fast -j16 && \
    echo "NVmain built"

# Hybrid build gem5 and NVmain
WORKDIR ../gem5
COPY /hybrid-build/SConscript /home/project/NVmain
COPY /hybrid-build/Options.py /home/project/gem5/configs/common
RUN scons EXTRAS=../NVmain build/X86/gem5.opt -j16 && \
    echo "gem5 and NVmain hybrid built"
RUN ./build/X86/gem5.opt configs/example/se.py -c tests/test-progs/hello/bin/x86/linux/hello \
    --cpu-type=TimingSimpleCPU --caches --l2cache --mem-type=NVMainMemory \
    --nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config && \
    echo "show test result" && \
    cat /home/project/gem5/m5out/stats.txt

# Copy some scripts
COPY hybrid-build-test.sh /home/project/gem5
WORKDIR ..
