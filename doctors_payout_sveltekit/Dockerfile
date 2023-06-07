FROM node:20.2-alpine3.18

LABEL maintainer='ahmed'


WORKDIR /doctors_payout_sveltekit

COPY ./ ./

EXPOSE 8007

ENV PATH="/doctors_payout_sveltekit/scripts:${PATH}"

CMD ["./scripts/node_run.sh"]