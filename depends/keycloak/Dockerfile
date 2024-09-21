FROM quay.io/keycloak/keycloak:25.0.6 as builder

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

ENV KC_DB=mariadb

WORKDIR /opt/keycloak
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:25.0.6
COPY --from=builder /opt/keycloak/ /opt/keycloak/


ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start", "--optimized"]
