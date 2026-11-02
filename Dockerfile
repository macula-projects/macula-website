FROM ghcr.io/gohugoio/hugo:v0.169.0

ENV PATH="/project/node_modules/.bin:${PATH}"
WORKDIR /project
USER root
RUN mkdir -p /project/node_modules && chown hugo:hugo /project/node_modules
USER hugo:hugo
