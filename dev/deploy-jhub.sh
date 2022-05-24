#!/bin/bash
helm --kubeconfig k3s.yaml upgrade --cleanup-on-fail --install jupyterhub jupyterhub/jupyterhub --namespace jupyterhub --create-namespace --version=1.2.0 --values jhub-config.yml
