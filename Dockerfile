FROM i386/ubuntu:cosmic

ARG DEBIAN_FRONTEND=noninteractive

RUN \
  apt-get update \
  && apt-get install -y --no-install-recommends apt-utils \
  && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
  cabal-install \
  ca-certificates \
  dnsutils \
  gcc \
  libgmp-dev \
  libssl-dev \
  ghc \
  git \
  openssl \
  zlib1g-dev \
  && cabal update

# COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sh"]
