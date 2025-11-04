# Cloud Attendance System — Final Version (Role-Based)

This package contains a COMPLETE, copy-paste implementation for a serverless Attendance Tracker on AWS.

## Components
- **Frontend (S3 hosted)**: HTML/CSS/JS (login, dashboard, attendance, QR, upload photo, history, analytics, manage users)
- **API Gateway**: HTTP API routes
- **Lambda (Python 3.9+)**: login, mark attendance, history, analytics, Excel/CSV export, S3 presigned upload
- **DynamoDB**:
  - `Users` (PK: username) → attributes: password, role (admin/faculty/student)
  - `Attendance` (PK: studentId, SK: date_time) → status, markedBy

## Setup (Quick)
1. Create DynamoDB tables:
   - **Users**: Partition key `username` (String)
   - **Attendance**: Partition key `studentId` (String), Sort key `date_time` (String)
2. Create S3 buckets:
   - Photos: `attendance-photos-yourname` (private)
   - Frontend: `attendance-frontend-yourname` (static website optional)
3. Create Lambda functions from files in `/lambdas` and connect API Gateway routes described in `api_routes.txt`.
4. In `/frontend/js/common.js`, set:
   ```js
   const API_BASE = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com";
   const PHOTO_BUCKET = "attendance-photos-yourname";
   ```
5. Upload `/frontend` files to your frontend S3 bucket.

## Security Notes
- Demo uses plaintext passwords for simplicity. For production, hash passwords (e.g., bcrypt) and use Cognito/JWT.
- All responses include CORS header `Access-Control-Allow-Origin: *` for ease of testing—tighten for production.
- Keep S3 buckets private. Photo uploads use **presigned PUT URLs**.

## Viva Talking Points
- Why Serverless (scalability, zero-maint, pay-per-use)
- Why DynamoDB over RDBMS (low-latency key access, autoscale)
- Presigned URLs for secure uploads (no credentials in browser)
- API Gateway + Lambda + CloudWatch logs
- Future scope: Rekognition face attendance, OTP login, CloudFront CDN

Good luck! 🚀
