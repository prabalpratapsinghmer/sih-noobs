# CI/CD — Jenkins + GitHub Actions

> Every push triggers: Build → Test → Image → Push → Deploy → Health → Notify.
> Jenkins is primary; GitHub Actions is backup for when Jenkins is down.

---

## 1. Jenkins Pipeline

```groovy
// devops/ci/Jenkinsfile
pipeline {
  agent any
  environment {
    REGISTRY = 'ghcr.io/sih26184'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Install & Lint') {
      steps {
        sh 'npm ci'
        sh 'npm run lint'
        sh 'npm run typecheck'
      }
    }
    stage('Unit Tests') {
      steps {
        sh 'npm run test -- --reporter=jest-junit'
      }
      post {
        always {
          junit 'test-results/**/*.xml'
        }
      }
    }
    stage('Build Frontends') {
      steps {
        sh 'npm run build'
      }
    }
    stage('Build Docker Images') {
      steps {
        sh '''
          docker build -t ${REGISTRY}/command-frontend:${IMAGE_TAG} -f apps/frontend-command/Dockerfile.command .
          docker build -t ${REGISTRY}/field-frontend:${IMAGE_TAG}   -f apps/frontend-field/Dockerfile.field .
          docker build -t ${REGISTRY}/admin-frontend:${IMAGE_TAG}   -f apps/frontend-admin/Dockerfile.admin .
        '''
      }
    }
    stage('Push to Registry') {
      steps {
        sh '''
          echo ${GHCR_TOKEN} | docker login ghcr.io -u ${REGISTRY} --password-stdin
          docker push ${REGISTRY}/command-frontend:${IMAGE_TAG}
          docker push ${REGISTRY}/field-frontend:${IMAGE_TAG}
          docker push ${REGISTRY}/admin-frontend:${IMAGE_TAG}
        '''
      }
    }
    stage('Deploy to Minikube') {
      steps {
        sh '''
          kubectl set image deployment/command-frontend command-frontend=${REGISTRY}/command-frontend:${IMAGE_TAG} -n sih26184
          kubectl set image deployment/field-frontend field-frontend=${REGISTRY}/field-frontend:${IMAGE_TAG} -n sih26184
          kubectl set image deployment/admin-frontend admin-frontend=${REGISTRY}/admin-frontend:${IMAGE_TAG} -n sih26184
          kubectl rollout status deployment/command-frontend -n sih26184 --timeout=120s
        '''
      }
    }
    stage('Health Check') {
      steps {
        sh '''
          sleep 5
          curl -sf http://localhost/command && echo "✅ Command OK" || exit 1
          curl -sf http://localhost/field   && echo "✅ Field OK"   || exit 1
          curl -sf http://localhost/admin   && echo "✅ Admin OK"   || exit 1
          curl -sf http://localhost/api/auth/me && echo "✅ Backend OK" || exit 1
        '''
      }
    }
  }
  post {
    success {
      discordSend(title: "✅ Build #${env.BUILD_NUMBER} GREEN", description: "All stages passed", color: "GREEN")
    }
    failure {
      discordSend(title: "❌ Build #${env.BUILD_NUMBER} RED", description: "Pipeline failed", color: "RED")
    }
  }
}
```

---

## 2. GitHub Actions (backup)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test
      - run: npm run build
      - name: Build Docker images
        run: |
          docker build -t ghcr.io/sih26184/command-frontend:ci -f apps/frontend-command/Dockerfile.command .
          docker build -t ghcr.io/sih26184/field-frontend:ci -f apps/frontend-field/Dockerfile.field .
          docker build -t ghcr.io/sih26184/admin-frontend:ci -f apps/frontend-admin/Dockerfile.admin .
```

---

## 3. Pipeline Stages Summary

| Stage | What runs | Fail gate |
|-------|-----------|-----------|
| Install & Lint | `npm ci`, `eslint`, `tsc --noEmit` | Lint errors, type errors |
| Unit Tests | `vitest` / `jest` | Test failures |
| Build Frontends | `vite build` for all apps | Build errors |
| Docker Images | `docker build` for each service | Build errors |
| Push Registry | Push to GitHub Container Registry | Auth failure |
| Deploy K8s | `kubectl set image` + rollout status | Rollout timeout |
| Health Check | `curl` each service | HTTP non-200 |
| Notify | Discord / Slack | — |

---

## 4. Triggers

| Trigger | Action |
|---------|--------|
| Push to `main` | Full pipeline → deploy to Minikube |
| Pull request | Build + test only (no deploy) |
| Manual | `Jenkinsfile` → "Build Now" |
| Tag `v*` | Full pipeline + tag images with version |

---

## 5. Pipeline Budget

Target: **< 10 minutes** from push to running.

| Stage | Estimated |
|-------|-----------|
| Install & Lint | 1 min |
| Unit Tests | 1.5 min |
| Build Frontends | 2 min |
| Docker Images | 2 min |
| Push Registry | 1.5 min |
| Deploy K8s | 1 min |
| Health Check | 0.5 min |
| **Total** | **~9.5 min** |
