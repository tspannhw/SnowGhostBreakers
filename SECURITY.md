# Security Policy

## 🔒 Security Best Practices

### Reporting Security Issues

If you discover a security vulnerability in this project, please report it privately by:

1. **DO NOT** create a public GitHub issue
2. Email the maintainers directly (or use GitHub Security Advisories)
3. Provide detailed information about the vulnerability
4. Allow reasonable time for the issue to be addressed

## 🛡️ Secure Configuration

### 1. Never Commit Credentials

**Never commit:**
- Snowflake passwords or private keys
- API keys or tokens
- Connection strings with credentials
- `.env` files with actual values
- Any file containing `password`, `secret`, or `api_key`

**Always use:**
- Environment variables
- `.env.example` as a template (committed)
- `.env` for actual credentials (gitignored)
- Snowflake key-pair authentication (recommended)

### 2. Snowflake Authentication

#### Option A: Username/Password (Basic)

```bash
# In .env file (never commit!)
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```

#### Option B: Key-Pair Authentication (Recommended)

```bash
# Generate key pair
openssl genrsa -out snowflake_private_key.pem 2048
openssl rsa -in snowflake_private_key.pem -pubout -out snowflake_public_key.pem

# Encrypt private key
openssl pkcs8 -topk8 -inform PEM -outform DER -in snowflake_private_key.pem \
  -out snowflake_private_key.p8 -nocrypt

# In .env file
SNOWFLAKE_PRIVATE_KEY_PATH=/secure/path/snowflake_private_key.p8
SNOWFLAKE_USER=your_username
```

Upload the public key to Snowflake:
```sql
ALTER USER your_username SET RSA_PUBLIC_KEY='MIIBIjANBg...';
```

#### Option C: OAuth or SSO (Enterprise)

Use Snowflake OAuth or SSO integration for enterprise deployments.

### 3. Least Privilege Access

Create a dedicated role with minimal permissions:

```sql
-- Create role with minimal permissions
CREATE ROLE GHOSTBUSTER;

-- Grant only necessary permissions
GRANT USAGE ON DATABASE GHOST_DETECTION TO ROLE GHOSTBUSTER;
GRANT USAGE ON SCHEMA GHOST_DETECTION.APP TO ROLE GHOSTBUSTER;
GRANT USAGE ON SCHEMA GHOST_DETECTION.ANALYTICS TO ROLE GHOSTBUSTER;

-- Grant SELECT on tables (read-only for analysts)
GRANT SELECT ON ALL TABLES IN SCHEMA GHOST_DETECTION.APP TO ROLE GHOSTBUSTER;
GRANT SELECT ON ALL VIEWS IN SCHEMA GHOST_DETECTION.ANALYTICS TO ROLE GHOSTBUSTER;

-- Grant EXECUTE on specific procedures only
GRANT USAGE ON PROCEDURE GHOST_DETECTION.APP.ASK_GHOST_DATABASE(STRING) TO ROLE GHOSTBUSTER;
GRANT USAGE ON PROCEDURE GHOST_DETECTION.APP.GENERATE_WEEKLY_REPORT() TO ROLE GHOSTBUSTER;

-- Grant role to user
GRANT ROLE GHOSTBUSTER TO USER your_username;
```

### 4. Network Security

- Use Snowflake's network policies to restrict IP addresses
- Enable MFA (Multi-Factor Authentication) for all users
- Use private connectivity (AWS PrivateLink, Azure Private Link, GCP Private Service Connect)

```sql
-- Example: Create network policy
CREATE NETWORK POLICY ghost_detection_policy
  ALLOWED_IP_LIST = ('192.168.1.0/24', '10.0.0.0/8')
  BLOCKED_IP_LIST = ('0.0.0.0/0');

-- Apply to user
ALTER USER your_username SET NETWORK_POLICY = ghost_detection_policy;
```

### 5. Secure Coding Practices

#### SQL Injection Prevention

**❌ DON'T:**
```python
# Never use string concatenation for SQL
query = f"SELECT * FROM GHOSTS WHERE ghost_name = '{user_input}'"
```

**✅ DO:**
```python
# Use parameterized queries
query = "SELECT * FROM GHOSTS WHERE ghost_name = ?"
session.sql(query, [user_input]).collect()
```

#### Environment Variables

**❌ DON'T:**
```python
password = "MyP@ssw0rd123"  # Never hardcode!
```

**✅ DO:**
```python
import os
password = os.getenv("SNOWFLAKE_PASSWORD")
if not password:
    raise ValueError("SNOWFLAKE_PASSWORD not set")
```

### 6. Secrets Management

#### Development
```bash
# Use .env file (local only, gitignored)
cp env.example .env
# Edit .env with your credentials
```

#### Production

Use a secrets manager:
- **AWS:** AWS Secrets Manager or Systems Manager Parameter Store
- **Azure:** Azure Key Vault
- **GCP:** Google Secret Manager
- **HashiCorp:** Vault
- **Snowflake:** External OAuth or Key-Pair Auth

Example with AWS Secrets Manager:
```python
import boto3
import json

def get_snowflake_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='ghost-detection/snowflake')
    return json.loads(response['SecretString'])
```

### 7. Audit and Monitoring

Enable Snowflake auditing:

```sql
-- Monitor login attempts
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
WHERE IS_SUCCESS = 'NO'
ORDER BY EVENT_TIMESTAMP DESC;

-- Monitor query history
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE USER_NAME = 'SUSPICIOUS_USER'
ORDER BY START_TIME DESC;

-- Monitor data access
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
WHERE OBJECT_NAME = 'GHOSTS'
ORDER BY QUERY_START_TIME DESC;
```

### 8. Data Protection

- Use Snowflake's encryption (automatic, AES-256)
- Enable column-level encryption for PII
- Use row-level security for sensitive data
- Implement data masking policies

```sql
-- Example: Masking policy for sensitive data
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ADMIN') THEN val
    ELSE '***MASKED***'
  END;

-- Apply to column
ALTER TABLE INVESTIGATORS MODIFY COLUMN email_address 
  SET MASKING POLICY email_mask;
```

## 🔍 Security Checklist

Before committing code:

- [ ] No hardcoded passwords or API keys
- [ ] All credentials use environment variables
- [ ] `.env` file is in `.gitignore`
- [ ] `env.example` provided as template
- [ ] SQL queries use parameterization
- [ ] Private keys are not committed
- [ ] Connection strings don't contain passwords
- [ ] Test with least-privilege role
- [ ] MFA enabled on Snowflake account
- [ ] Review git history for accidentally committed secrets

## 🚨 If Credentials Are Leaked

If credentials are accidentally committed:

1. **Immediately rotate the credentials**
   ```sql
   ALTER USER your_username SET PASSWORD = 'NewSecurePassword';
   ```

2. **Remove from git history**
   ```bash
   # Use BFG Repo-Cleaner or git filter-branch
   bfg --replace-text passwords.txt
   git push --force
   ```

3. **Review access logs**
   ```sql
   SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
   WHERE USER_NAME = 'compromised_user'
   AND EVENT_TIMESTAMP > 'timestamp_of_leak';
   ```

4. **Notify affected parties**

## 📚 Additional Resources

- [Snowflake Security Best Practices](https://docs.snowflake.com/en/guides-overview-security)
- [Snowflake Key-Pair Authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## 📞 Contact

For security concerns, contact: [Your Security Contact]

---

**Remember:** Security is everyone's responsibility. When in doubt, ask!

