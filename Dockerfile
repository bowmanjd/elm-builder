FROM {base}

ARG DEBIAN_FRONTEND=noninteractive

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /work

RUN apt-get update \
  && apt-get install -y --no-install-recommends apt-utils \
  && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  ca-certificates \
  curl \
  g++ \
  gcc \
  git \
  libc6-dev \
  libffi-dev \
  libgmp-dev \
  libncurses5 \
  libncurses5-dev \
  make \
  netbase \
  openssl \
  xz-utils \
  zlib1g-dev \
  && curl -fSL https://get.haskellstack.org/stable/linux-{arch}.tar.gz \
  -o /stack.tar.gz \
  && curl -fSL https://github.com/elm/compiler/archive/0.19.0.tar.gz \
  -o /elm.tar.gz \
  && apt-get purge -y --auto-remove curl \
  && tar -xf /stack.tar.gz -C /usr/local/bin --strip-components=1 \
  && /usr/local/bin/stack config set system-ghc --global false \
  && /usr/local/bin/stack config set install-ghc --global true \
  && tar -xf /elm.tar.gz -C /work --strip-components=1 \
  && rm -rf /var/lib/apt/lists/* /stack.tar.gz /elm.tar.gz

CMD ["bash"]
