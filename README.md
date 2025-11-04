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

