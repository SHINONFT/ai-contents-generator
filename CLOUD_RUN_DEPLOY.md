# Cloud Run デプロイ手順

## 前提条件

- Google Cloud CLIがインストール済み
- GCPプロジェクトが作成済み
- 課金が有効化済み

## 環境変数の設定

Cloud Runにデプロイする前に、以下の環境変数を設定してください：

```bash
# GCPプロジェクトIDを設定
export PROJECT_ID=your-gcp-project-id
```

## デプロイ方法

### 方法1: Cloud Buildを使用（推奨）

```bash
gcloud builds submit --config cloudbuild.yaml --project $PROJECT_ID
```

### 方法2: 手動デプロイ

```bash
# Dockerイメージをビルド
docker build -t gcr.io/$PROJECT_ID/ai-content-generator .

# Container Registryにプッシュ
docker push gcr.io/$PROJECT_ID/ai-content-generator

# Cloud Runにデプロイ
gcloud run deploy ai-content-generator \
  --image gcr.io/$PROJECT_ID/ai-content-generator \
  --region asia-northeast1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

## 環境変数の設定（Cloud Run）

デプロイ後、Cloud Runの環境変数を設定してください：

```bash
gcloud run services update ai-content-generator \
  --region asia-northeast1 \
  --set-env-vars "\
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_key,\
CLERK_SECRET_KEY=your_clerk_secret,\
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in,\
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up,\
NEXT_PUBLIC_GOOGLE_GEMINI_API_KEY=your_gemini_key,\
NEXT_PUBLIC_DRIZZLE_DB_URL=your_neon_db_url,\
NEXT_PUBLIC_POSTHOG_KEY=your_posthog_key,\
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com"
```
