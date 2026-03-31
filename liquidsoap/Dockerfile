FROM savonet/liquidsoap:v2.3.1

ENV DEBIAN_FRONTEND=noninteractive
USER root

RUN apt-get update && apt-get install -y python3-mutagen && rm -rf /var/lib/apt/lists/*

COPY gen_playlists.py /etc/liquidsoap/gen_playlists.py
COPY entrypoint.sh /entrypoint.sh
RUN chown -R liquidsoap /etc/liquidsoap

USER liquidsoap
ENTRYPOINT "/entrypoint.sh"
