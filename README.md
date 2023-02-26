# `pembundle2jks`

Convert a PEM bundle or three into a JKS.

### How I Use?

This was made for use with Keycloak and trust-manager.  When Keycloak starts, it runs this
container to convert the CA bundle provided by trust-manager from an init container.

It can, of course, be used separately via Docker or using python directly.

This fragment describes how to use an init container and a shared volume to override the
system cacerts file in the keycloak image (as of this commit, anyway).

```
using configMap ca-bundle
-> mount in create-ca-jks                   /etc/ssl/certs/ca-bundle.crt
-> create jks in shared emptyDir            /ca-transfer/ca-bundle.jks
-> mount shared emptyDir in keycloak over   /etc/pki/ca-trust/extrated/java/cacerts

      initContainers:
      - name: create-ca-jks
        command: ["pembundle2jks", "-o", "/ca-transfer/ca-bundle.jks", "/etc/ssl/certs/ca-bundle.crt"]
        image: jamesandariese/pembundle2jks
        volumeMounts:
        - mountPath: /etc/ssl/certs/ca-bundle.crt
          name: ca-bundle
          subPath: ca-bundle.crt
        - mountPath: /ca-transfer
          name: ca-transfer
      containers:
      - name: keycloak
        args:
        - start
        volumeMounts:
        - mountPath: /etc/ssl/certs/ca-bundle.crt
          name: ca-bundle
          subPath: ca-bundle.crt
        - mountPath: /etc/pki/ca-trust/extracted/java/cacerts
          name: ca-transfer
          subPath: ca-bundle.jks
      volumes:
      - name: ca-bundle
        configMap:
          name: ca-bundle
      - name: ca-transfer
        emptyDir:
          medium: Memory
          sizeLimit: 50Mi
```
