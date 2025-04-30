# Security Policy

## Supported Versions

The following table shows which versions of `fastapi-amis-admin` are currently supported with security updates:

| Version | Supported |
|---------|-----------|
| 0.7.x   | ✅ Yes     |
| < 0.7.0 | ❌ No      |

Please always use the latest release for maximum stability and security.

---

## Reporting a Vulnerability

If you discover a security vulnerability in `fastapi-amis-admin`, we **strongly encourage** you to report it privately and responsibly.

### 🔐 Private Disclosure Process

Please send detailed information to:

**📧 Email:** `amisadmin@protonmail.com`  
(Or use [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing) for private reporting.)

Include:

- Description of the vulnerability
- A minimal reproducible example if applicable
- Impact and potential risks
- Any suggested fixes or mitigation steps

We aim to respond to all reports within **5 business days** and resolve confirmed issues promptly.

---

## Public Disclosure

Please **do not disclose security issues publicly** until they are fully patched and a release has been made. We appreciate your cooperation in protecting users.

---

## Security Best Practices

When using `fastapi-amis-admin`, we recommend:

- Always updating to the latest version.
- Validating and sanitizing user inputs.
- Using HTTPS for production deployments.
- Managing secrets securely (avoid hardcoding credentials).
- Regularly reviewing dependencies with `pip-audit`, `safety`, or `dependabot`.

---

## Credits

Thanks to all security researchers and community contributors who help keep this project safe and secure. 🛡️

---

## License

This project is licensed under the [Apache 2.0 License](./LICENSE).
