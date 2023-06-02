FROM node:20-alpine3.16

LABEL maintainer='ahmed'


WORKDIR /doctors_payout_sveltekit


COPY ./ ./


# RUN npm install -g npm@9.6.7 \
#     && npm ci  \
#     && chmod -R 777 /doctor_payout_sveltekit

EXPOSE 8007

ENV VITE_DJANGO_BASE_URL=http://172.20.100.81:8008

ENV HOST=0.0.0.0
ENV PORT=8007

ENV PATH="/doctors_payout_sveltekit/scripts:${PATH}"

CMD ["./scripts/node_run.sh"]